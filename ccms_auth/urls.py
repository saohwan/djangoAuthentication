from django.urls import path

from ccms_auth.views import LoginView, PasswordChangeView, RegistrationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('register/', RegistrationView.as_view(), name='register'),
]
