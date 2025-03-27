from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/xero/', include('xero_auth.urls')),
    path('api/v1/xero/accounts/', include('xero_data.urls')),
]

