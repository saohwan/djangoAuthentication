from django.contrib import admin
from django.urls import re_path, path, include
from rest_framework import routers

import ccms_auth

# router = routers.DefaultRouter()
# router.register('auth', )

urlpatterns = [
    # re_path('admin/', admin.site.urls),
    # re_path('1', views.login),
    # re_path('2', views.signup),
    # re_path('test_token', views.test_token)
    path('admin/', admin.site.urls),
    path('api/', include('ccms_auth.urls'))
]
