# persons/urls.py:1
from django.urls import path, re_path

from persons.views import UserLoginView, UsersRegistrationView

# from persons.views import  UsersRegistrationView
from persons.views.views_register import UsersVerificationDuringRegistration

urlpatterns = [
    re_path(
        r"^register/(?P<role>account|moderators|client|manager|admin)/$",
        UsersRegistrationView.as_view(),
        name="management",
    ),  # name="management"
    re_path(
        r"^register/$",
        UsersRegistrationView.as_view(),
        name="token",
    ),
    path(
        "register/verification/",
        UsersVerificationDuringRegistration.as_view(),
        name="register_token",
    ),
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",  # wagtailadmin_login
    ),
]
