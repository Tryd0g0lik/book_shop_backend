# persons/urls.py:1
from django.urls import path, re_path

from persons.test.get_request.test_get_csrftoken_token import test_get_csrf_token
from persons.views import UserLoginView, UsersRegistrationView
from persons.views.test_email import test_email_view
from persons.views.views_register import UsersVerificationDuringRegistration

urlpattern = [
    path("test-email/", test_email_view, name="test_email"),
    path("test_email/", test_get_csrf_token, name="test_csrf_toke"),
    path(
        "register/verification/",
        UsersVerificationDuringRegistration.as_view(),
        name="register_token",
    ),
    re_path(
        "^register/(account/|moderator/|manager/|admin/)?$",
        UsersRegistrationView.as_view(),
        name="management",
    ),  # name="management"
    re_path(
        "login/$",
        UserLoginView.as_view(),
        name="account_login",
    ),
]
