from django.contrib import admin
from django.urls import path
from xero_auth.views import XeroLogin, XeroCallback, RefreshXeroTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("xero/login/", XeroLogin.as_view(), name="xero_login"),
    path("auth/callback/", XeroCallback.as_view(), name="xero_callback"),
    path("auth/refresh/", RefreshXeroTokenView.as_view(), name="xero_refresh"),
]

