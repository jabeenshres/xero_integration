import requests
from datetime import timedelta
from django.shortcuts import redirect
from django.utils.timezone import now
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from xero_auth.models import XeroToken
from xero_auth.helpers import get_xero_tenant


class XeroLogin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_url = (
            f"{settings.XERO_AUTH_URL}"
            f"?response_type=code&client_id={settings.XERO_CONFIG['CLIENT_ID']}"
            f"&redirect_uri={settings.XERO_CONFIG['REDIRECT_URI']}"
            f"&scope={' '.join(settings.XERO_CONFIG['SCOPES'])}"
        )
        return redirect(auth_url)

class XeroCallback(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Authorization code missing"}, status=400)

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.XERO_CONFIG['REDIRECT_URI'],
            "client_id": settings.XERO_CONFIG['CLIENT_ID'],
            "client_secret": settings.XERO_CONFIG['CLIENT_SECRET'],
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Use environment variable for token URL
        response = requests.post(
            settings.XERO_TOKEN_URL,
            data=data,
            headers=headers
        )
        
        if response.status_code != 200:
            return Response({"error": "Failed to retrieve tokens"}, status=response.status_code)

        token_data = response.json()
        
        # Use environment variable for connections URL
        tenant_response = requests.get(
            settings.XERO_CONNECTIONS_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )

        if tenant_response.status_code != 200:
            return Response({"error": "Failed to retrieve tenant ID"}, status=tenant_response.status_code)

        tenants = tenant_response.json()
        if not tenants:
            return Response({"error": "No tenant ID found"}, status=400)

        XeroToken.objects.update_or_create(
            tenant_id=tenants[0]["tenantId"],
            defaults={
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": now() + timedelta(seconds=token_data["expires_in"]),
            },
        )

        return Response({"message": "Xero authentication successful"})

class RefreshXeroTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token, tenant_id = get_xero_tenant()
        if not access_token or not tenant_id:
            return Response({"error": "Failed to refresh token"}, status=401)
        return Response({"message": "Token refreshed successfully"})

# Helper function optimization
