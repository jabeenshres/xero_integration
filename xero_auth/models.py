import logging
import requests

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

from django.contrib.auth import get_user_model

# Get logger instance
logger = logging.getLogger('xero_auth')

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
        """Refresh the access token if it's expired or about to expire"""
        try:
            # Add buffer time to avoid race conditions
            if self.expires_at > now() + timedelta(minutes=5):
                logger.debug(f"Token still valid for user {self.user.id}")
                return self.access_token

            logger.info(f"Refreshing token for user {self.user.id}")
            
            response = requests.post(
                settings.XERO_TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": settings.XERO_CONFIG['CLIENT_ID'],
                    "client_secret": settings.XERO_CONFIG['CLIENT_SECRET'],
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            self.expires_at = now() + timedelta(seconds=token_data["expires_in"])
            self.save()
            
            logger.info(f"Successfully refreshed token for user {self.user.id}")
            return self.access_token

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Token refresh failed for user {self.user.id}: {str(e)}",
                exc_info=True,
                extra={
                    'user_id': self.user.id,
                    'tenant_id': self.tenant_id,
                    'error_details': str(e.response.json()) if hasattr(e, 'response') else None
                }
            )
            return None

        except Exception as e:
            logger.critical(
                f"Unexpected error during token refresh for user {self.user.id}: {str(e)}",
                exc_info=True
            )
            return None