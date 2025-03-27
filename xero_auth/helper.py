import requests
from xero_auth.models import XeroToken

def get_xero_tenant():
    """
    Retrieves the latest Xero tenant ID.
    """
    token = XeroToken.objects.first()
    if not token:
        return None, None

    access_token = token.refresh_token_if_needed()
    if not access_token:
        return None, None

    url = "https://api.xero.com/connections"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None, None

    tenants = response.json()
    if not tenants:
        return None, None

    return access_token, tenants[0]["tenantId"]