from django.urls import path
from xero_auth.views import XeroLogin, XeroCallback, RefreshXeroTokenView

app_name = 'xero-auth'

urlpatterns = [
    path("login/", XeroLogin.as_view(), name="xero_login"),
    path("callback/", XeroCallback.as_view(), name="xero_callback"),
    path("refresh/", RefreshXeroTokenView.as_view(), name="xero_refresh"),
]

