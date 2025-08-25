from django.urls import path
from .views import UserBalanceView, SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("balance/", UserBalanceView.as_view(), name="user-balance"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/introspect/", TokenVerifyView.as_view(), name="token_verify"),
]
