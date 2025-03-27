from django.contrib import admin
from django.urls import path
from xero_auth.views import XeroLogin, XeroCallback


urlpatterns = [
    path('admin/', admin.site.urls),
    path("xero/login/", XeroLogin.as_view(), name="xero_login"),
    path("auth/callback/", XeroCallback.as_view(), name="xero_callback"),
]

