import logging
from datetime import timedelta

from django.conf.global_settings import SERVER_EMAIL

from persons.apps import DEBUG
from project.settings import JWT_SECRET_KEY

# from logs import configure_logging
from project.settings_conf.settings_env import (
    APP_DEFAULT_FROM_EMAIL,
    APP_EMAIL_HOST,
    APP_EMAIL_HOST_PASSWORD,
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES,
    JWT_REFRESH_TOKEN_LIFETIME_DAYS,
)

# configure_logging(logging.INFO)
log = logging.getLogger(__name__)

# ============================================
# CORS
# ============================================
# False - this is the default value which means that the server doesn't accept data from other sources.
CORS_ORIGIN_ALLOW_ALL = False
# Here, we allow the URL list for publicated
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8081",
    "http://localhost:8081",
    "http://83.166.245.209:8001",
]

# https://github.com/adamchainz/django-cors-headers?tab=readme-ov-file#csrf-integration
# https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS
# This is list from private of URL
CSRF_TRUSTED_ORIGINS = [*CORS_ALLOWED_ORIGINS]
# Allow the cookie in HTTP request.
CORS_ALLOW_CREDENTIALS = True
# Allow the methods to the methods in HTTP
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "Authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Accept-Language",
    "Content-Language",
]

# PASSWORD_RESET_TIMEOUT_DAYS = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/

# ============================================
# REST_FRAMEWORK SETTINGS AND JWT-tokens
# ============================================
# https://pypi.org/project/djangorestframework-simplejwt/4.3.0/
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/stateless_user_authentication.html
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # This for works with sessions
        "rest_framework.authentication.TokenAuthentication",  # Options for API
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(JWT_ACCESS_TOKEN_LIFETIME_MINUTES)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(JWT_REFRESH_TOKEN_LIFETIME_DAYS)),
    "SIGNING_KEY": JWT_SECRET_KEY[:25],
    # "TOKEN_OBTAIN_SERIALIZER": "persons.views.serializers.token_obtain_serializer.TokenObtainPairSerializer",
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS": "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED": "rest_framework_simplejwt.serializers.default_on_login_failed",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    # "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    "CHECK_REVOKE_TOKEN": False,
    "REVOKE_TOKEN_CLAIM": "hash_password",
    "CHECK_USER_IS_ACTIVE": True,
}


# ============================================
# EMAIL AUTHENTIFICATION OF USER
# ============================================
# WAGTAILUSERS_PASSWORD_ENABLED - That will disable the password for Wagtail
WAGTAILUSERS_PASSWORD_ENABLED = False
# Django settings of the email aut.

if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST_USER = ""
    EMAIL_HOST = APP_EMAIL_HOST
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = APP_EMAIL_HOST_PASSWORD
    DEFAULT_FROM_EMAIL = (
        APP_DEFAULT_FROM_EMAIL if APP_DEFAULT_FROM_EMAIL else SERVER_EMAIL
    )


# Time live of the magic refer
# MAGIC_TOKEN_TIMEOUT = 300
# ============================================
# ALLAUTH
# ============================================
# Make sure "webauthn" is included.
MFA_SUPPORTED_TYPES = ["totp", "webauthn", "recovery_codes"]
# Optional: enable support for logging in using a (WebAuthn) passkey.
MFA_PASSKEY_LOGIN_ENABLED = True
ACCOUNT_EMAIL_UNIQUE = True
# SOCIALACCOUNT_PROVIDERS = {}
# # The maximum amount of email addresses a user can associate to his account
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
# # The user is blocked from logging in until the email address is verified
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# Defense from  lot quantity  entering  the password
# ACCOUNT_RATE_LIMITS = {
#     "reset_password": "3/20/ip",
#     "login": "3/10m/ip",
#     "login_failed": "5/5m",  # 5 incorrect re-entries 5m.
#     "email_confirmation": "3/10m",  # 3 configuration an email on the 10м.
# }
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
# Controls whether password reset is performed by means of following a link in \
# the email (False), or by entering a code (True).
ACCOUNT_PASSWORD_RESET_BY_CODE_EABLED = False
#
# # Require a password before the account remove
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Shop] "
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

ACCOUNT_FORMS = {
    "signup": "persons.forms.users_registration_form.UsersRegistrationForm",
    "login": "persons.forms.login_form.UsersLoginForm",
}
