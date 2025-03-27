# xero_auth/models.py
import requests
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class XeroToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='xero_tokens'
    )
    tenant_id = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'tenant_id')
    
    def refresh_token_if_needed(self):
        """Refresh the access token if it's expired"""
        if self.expires_at > now():
            return self.access_token  # Token is still valid

        token_url = "https://identity.xero.com/connect/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": settings.XERO_CONFIG['CLIENT_ID'],
            "client_secret": settings.XERO_CONFIG['CLIENT_SECRET'],
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(token_url, data=data, headers=headers)
        if response.status_code != 200:
            return None  # Token refresh failed

        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]
        self.expires_at = now() + timedelta(seconds=token_data["expires_in"])
        self.save()

        return self.access_token