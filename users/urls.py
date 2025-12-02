from django.urls import path
from .views import RegisterUser, LoginUser, ProfileUser, LogoutUser
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("profile/", ProfileUser.as_view(), name="profile"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutUser.as_view(), name="logout"),
]
