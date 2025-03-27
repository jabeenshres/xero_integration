
# xero_integration/views.py
import requests
from datetime import timedelta
from django.shortcuts import redirect
from django.utils.timezone import now
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from xero_auth.models import XeroToken

class XeroLogin(APIView):
    def get(self, request):
        auth_url = (
            "https://login.xero.com/identity/connect/authorize"
            f"?response_type=code&client_id={settings.XERO_CONFIG['CLIENT_ID']}"
            f"&redirect_uri={settings.XERO_CONFIG['REDIRECT_URI']}&scope={' '.join(settings.XERO_CONFIG['SCOPES'])}"
        )
        return redirect(auth_url)

class XeroCallback(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Authorization code missing"}, status=400)

        token_url = "https://identity.xero.com/connect/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.XERO_CONFIG['REDIRECT_URI'],
            "client_id": settings.XERO_CONFIG['CLIENT_ID'],
            "client_secret": settings.XERO_CONFIG['CLIENT_SECRET'],
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(token_url, data=data, headers=headers)
        if response.status_code != 200:
            return Response({"error": "Failed to retrieve tokens"}, status=response.status_code)

        token_data = response.json()
        XeroToken.objects.update_or_create(
            tenant_id="default",
            defaults={
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": now() + timedelta(seconds=token_data["expires_in"]),
            },
        )
        return Response({"message": "Xero authentication successful"})
