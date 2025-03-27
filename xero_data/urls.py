from django.urls import path
from xero_data.views import FetchChartOfAccounts

app_name = 'xero_data'

urlpatterns = [
    path("fetch/", FetchChartOfAccounts.as_view(), name="fetch_accounts"),
]