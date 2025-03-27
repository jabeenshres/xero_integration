from django.db import models

class XeroAccount(models.Model):
    account_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    tax_type = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name