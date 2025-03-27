from rest_framework import serializers
from .models import XeroAccount

class XeroAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeroAccount
        fields = '__all__'

    def to_internal_value(self, data):
        # Transform Xero field names to model field names
        field_map = {
            'AccountID': 'account_id',
            'Code': 'code',
            'Name': 'name',
            'Type': 'type',
            'TaxType': 'tax_type',
            'Status': 'status',
            'Description': 'description',
            'Class': 'class_type',
            'SystemAccount': 'system_account',
            'EnablePaymentsToAccount': 'enable_payments_to_account',
            'ShowInExpenseClaims': 'show_in_expense_claims',
            'BankAccountType': 'bank_account_type',
            'ReportingCode': 'reporting_code',
            'ReportingCodeName': 'reporting_code_name',
            'HasAttachments': 'has_attachments',
            'UpdatedDateUTC': 'updated_date_utc',
            'AddToWatchlist': 'add_to_watchlist'
        }
        return {
            model_field: data.get(xero_field)
            for xero_field, model_field in field_map.items()
        }