# xero_integration/models.py
from django.db import models

class XeroToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    tenant_id = models.CharField(max_length=255)

    def __str__(self):
        return f"XeroToken for Tenant {self.tenant_id}"