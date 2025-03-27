from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from xero_data.models import XeroAccount
from xero_data.serializers import XeroAccountSerializer
import datetime
from xero_auth.helper import get_xero_tenant


# --- Helper functions (place these above your view class) ---

def parse_xero_date(xero_date_str):
    """Optimized date parser"""
    if not xero_date_str:
        return None
    try:
        millis = int(xero_date_str.split('(')[1].split(')')[0].split('+')[0].split('-')[0])
        return datetime.datetime.fromtimestamp(millis/1000.0)
    except (ValueError, IndexError, AttributeError):
        return None

def transform_xero_account(account_data):
    """Fast field mapping using static tuple"""
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

# --- View Class ---

class XeroAccountView(APIView):
    def get(self, request):
        # 1. Authentication
        access_token, tenant_id = get_xero_tenant()
        if not access_token or not tenant_id:
            return Response({"error": "Failed to authenticate with Xero"}, status=401)

        # 2. API Request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Xero-Tenant-Id": tenant_id,
            "Accept": "application/json"
        }
        response = requests.get("https://api.xero.com/api.xro/2.0/Accounts", headers=headers)
        
        if response.status_code != 200:
            return Response({"error": "Failed to fetch accounts"}, status=response.status_code)

        # 3. Data Processing
        accounts_data = response.json().get("Accounts", [])
        
        # Pre-get existing IDs for faster lookup
        existing_ids = set(XeroAccount.objects.values_list('account_id', flat=True))
        
        # Prepare batch operations
        to_create = []
        to_update = []
        
        for account in accounts_data:
            transformed = transform_xero_account(account)
            if transformed['account_id'] in existing_ids:
                to_update.append(transformed)
            else:
                to_create.append(transformed)
        
        # 4. Bulk Database Operations
        with transaction.atomic():
            # Create new accounts
            if to_create:
                XeroAccount.objects.bulk_create(
                    [XeroAccount(**data) for data in to_create],
                    batch_size=500
                )
            
            # Update existing accounts
            for account in to_update:
                XeroAccount.objects.filter(account_id=account['account_id']).update(**account)
        
        # 5. Return Response
        serializer = XeroAccountSerializer(
            XeroAccount.objects.all(),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)