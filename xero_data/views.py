import requests
import logging
import datetime

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from requests.exceptions import RequestException
from xero_data.models import XeroAccount
from xero_data.serializers import XeroAccountSerializer
from xero_auth.helpers import get_xero_tenant

logger = logging.getLogger('xero_auth')

def parse_xero_date(xero_date_str):
    """Parse Xero's special date format (/Date(123456789+0000)/)"""
    if not xero_date_str:
        return None
    try:
        millis = int(xero_date_str.split('(')[1].split(')')[0].split('+')[0].split('-')[0])
        return datetime.datetime.fromtimestamp(millis/1000.0)
    except (ValueError, IndexError, AttributeError):
        logger.warning(f"Failed to parse Xero date: {xero_date_str}")
        return None

def transform_xero_account(account_data):
    """Transform Xero API account data to our model fields"""
    field_map = (
        ('AccountID', 'account_id'),
        ('Code', 'code'),
        ('Name', 'name'),
        ('Type', 'type'),
        ('TaxType', 'tax_type'),
        ('Status', 'status'),
        ('Description', 'description'),
        ('Class', 'class_type'),
        ('SystemAccount', 'system_account'),
        ('EnablePaymentsToAccount', 'enable_payments_to_account'),
        ('ShowInExpenseClaims', 'show_in_expense_claims'),
        ('BankAccountType', 'bank_account_type'),
        ('ReportingCode', 'reporting_code'),
        ('ReportingCodeName', 'reporting_code_name'),
        ('HasAttachments', 'has_attachments'),
        ('AddToWatchlist', 'add_to_watchlist')
    )
    
    transformed = {}
    for xero_field, model_field in field_map:
        if xero_field in account_data:
            transformed[model_field] = account_data[xero_field]
    
    transformed['updated_date_utc'] = parse_xero_date(account_data.get('UpdatedDateUTC'))
    return transformed

class XeroAccountView(APIView):
    """
    Retrieve and store Xero Chart of Accounts
    
    GET /xero/accounts/
    - Fetches accounts from Xero API
    - Stores/updates in local database
    - Returns all accounts for the authenticated user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # 1. Authentication
            access_token, tenant_id = get_xero_tenant()
            if not access_token or not tenant_id:
                logger.error("Xero authentication failed - missing token or tenant ID")
                return Response(
                    {"error": "Failed to authenticate with Xero"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 2. API Request
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Xero-Tenant-Id": tenant_id,
                "Accept": "application/json"
            }
            
            try:
                logger.info(f"Fetching accounts from Xero API for user {user.id}")
                response = requests.get(
                    settings.XERO_ACCOUNTS,
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                accounts_data = response.json().get("Accounts", [])
                logger.info(f"Received {len(accounts_data)} accounts from Xero")
                
            except RequestException as e:
                logger.error(f"Xero API request failed for user {user.id}: {str(e)}")
                return Response(
                    {"error": "Failed to fetch accounts from Xero"}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            # 3. Prepare database operations
            existing_accounts = XeroAccount.objects.filter(user=user)
            existing_ids = set(existing_accounts.values_list('account_id', flat=True))
            
            to_create = []
            to_update = []
            
            for account in accounts_data:
                transformed = transform_xero_account(account)
                if not transformed.get('account_id'):
                    continue
                    
                # Add user to the transformed data
                transformed['user'] = user
                
                if transformed['account_id'] in existing_ids:
                    to_update.append(transformed)
                else:
                    to_create.append(transformed)

            # 4. Execute database operations
            with transaction.atomic():
                # Bulk create new accounts
                if to_create:
                    XeroAccount.objects.bulk_create(
                        [XeroAccount(**data) for data in to_create],
                        batch_size=500
                    )
                    logger.info(f"Created {len(to_create)} new accounts for user {user.id}")
                
                # Bulk update existing accounts
                if to_update:
                    update_instances = []
                    for account in to_update:
                        obj = XeroAccount.objects.get(
                            user=user,
                            account_id=account['account_id']
                        )
                        for field, value in account.items():
                            if field != 'account_id':
                                setattr(obj, field, value)
                        update_instances.append(obj)
                    
                    XeroAccount.objects.bulk_update(
                        update_instances,
                        fields=[f.name for f in XeroAccount._meta.fields 
                               if f.name not in ['id', 'account_id', 'user']],
                        batch_size=500
                    )
                    logger.info(f"Updated {len(to_update)} existing accounts for user {user.id}")

            # 5. Return response with only user's accounts
            serializer = XeroAccountSerializer(
                XeroAccount.objects.filter(user=user),
                many=True
            )
            
            return Response({
                "status": "success",
                "accounts_created": len(to_create),
                "accounts_updated": len(to_update),
                "total_accounts": XeroAccount.objects.filter(user=user).count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.critical(
                f"Unexpected error in XeroAccountView for user {user.id}: {str(e)}", 
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )