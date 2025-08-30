from django.urls import path
from .views import CustomLoginView, UserBalanceView, SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("balance/", UserBalanceView.as_view(), name="user-balance"),
    path("token/", CustomLoginView.as_view(), name="custom_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/introspect/", TokenVerifyView.as_view(), name="token_verify"),
]
