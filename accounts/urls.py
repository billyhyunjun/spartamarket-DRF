from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "accounts"

urlpatterns = [
    path("", views.AccountAPI.as_view(), name="accounts"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("password/", views.password, name="password"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("<str:username>/", views.AccountUserAPI.as_view(), name="profile"),
]
