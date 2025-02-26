from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                         ResetPasswordConfirmView, UserUpdateView, UserCreateAPIView, BalanceView,
                         SendVerificationCodeAPIView, CheckActivationCodePayAPIView)

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view()),
    path('register-step2', UserCreateAPIView.as_view()),
    path('register-activate-code', CheckActivationCodeGenericAPIView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
    path('reset-password-confirm', ResetPasswordConfirmView.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('login-refresh', TokenRefreshView.as_view()),
    path('profile', UserUpdateView.as_view(), name='user-update'),
    path('balance', BalanceView.as_view(), name='user-update'),
    path("send-verification-code", SendVerificationCodeAPIView.as_view(), name="send-verification-code"),
    path("check-verification-code", CheckActivationCodePayAPIView.as_view(), name="check-activation-code"),
]