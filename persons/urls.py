# persons/urls.py:1
from django.urls import path, re_path

from persons.test.get_request.test_get_csrftoken_token import test_get_csrf_token
from persons.views import UserLoginView, UsersRegistrationView
from persons.views.test_email import test_email_view
from persons.views.views_register import UsersVerificationDuringRegistration

urlpatterns = [
    re_path(
        "^register/(?:account/moderator|manager|admin)/$",
        UsersRegistrationView.as_view(),
        name="management",
    ),  # name="management"
    path(
        "register/verification/",
        UsersVerificationDuringRegistration.as_view(),
        name="register_token",
    ),
    path(
        "register/",
        UsersRegistrationView.as_view(),
        name="management",
    ),
    re_path(
        "login/$",
        UserLoginView.as_view(),
        name="account_login",
    ),
]
