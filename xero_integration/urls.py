from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # User authentication
    path('api/v1/auth/', include('authentication.urls')),

    # User authorization to Xero
    path('api/v1/xero/', include('xero_auth.urls')),
    path('api/v1/xero/accounts/', include('xero_data.urls')),
]

