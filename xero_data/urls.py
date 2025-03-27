from django.urls import path
from xero_data.views import XeroAccountView

app_name = 'xero_data'

urlpatterns = [
    path("fetch/", XeroAccountView.as_view(), name="fetch_accounts"),
]