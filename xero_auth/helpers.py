import requests
from django.conf import settings
from xero_auth.models import XeroToken

def get_xero_tenant():
    """Optimized tenant retrieval with cached headers"""
    token = XeroToken.objects.first()
    if not token:
        return None, None

    access_token = token.refresh_token_if_needed()
    if not access_token:
        return None, None

    response = requests.get(
        settings.XERO_CONNECTIONS_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if response.status_code == 200 and (tenants := response.json()):
        return access_token, tenants[0]["tenantId"]
    
    return None, None