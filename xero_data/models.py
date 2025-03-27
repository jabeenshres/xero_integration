from django.db import models


from django.contrib.auth import get_user_model

# Get logger instance

User = get_user_model()

class XeroAccount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='account_data'
    )
    account_id = models.CharField(max_length=50, unique=True)  # Xero's AccountID
    code = models.CharField(max_length=50, null=True, blank=True)  # Account Code
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    tax_type = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)  # ACTIVE/ARCHIVED
    description = models.TextField(null=True, blank=True)
    class_type = models.CharField(max_length=50, null=True, blank=True)  # Account Class
    system_account = models.CharField(max_length=50, null=True, blank=True)  # SYSTEM ACC
    enable_payments_to_account = models.BooleanField(default=False)
    show_in_expense_claims = models.BooleanField(default=False)
    bank_account_type = models.CharField(max_length=50, null=True, blank=True)
    reporting_code = models.CharField(max_length=50, null=True, blank=True)
    reporting_code_name = models.CharField(max_length=255, null=True, blank=True)
    has_attachments = models.BooleanField(default=False)
    updated_date_utc = models.DateTimeField(null=True, blank=True)  # Xero's UpdatedDateUTC
    add_to_watchlist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.code})"