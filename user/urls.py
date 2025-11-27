from django.urls import path
from .views import RegisterUser, LoginUser, ProfileUser

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("profile/", ProfileUser.as_view(), name="profile"),
]
