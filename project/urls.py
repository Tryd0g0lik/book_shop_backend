"""
URL configuration for backend.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from persons.test.get_request.test_get_csrftoken_token import test_get_csrf_token
from persons.views import UserLoginView, UsersRegistrationView
from persons.views.test_email import test_email_view
from persons.views.views_register import UsersVerificationDuringRegistration
from project import settings
from project.settings_conf.settings_env import APP_NAME

schema_view = get_schema_view(
    openapi.Info(
        title=APP_NAME,
        default_version="v1",
        description="Shop of good sale",
        contact=openapi.Contact(email="work80@mail.ru"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    patterns=[],
)

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls), name="admin-panel"),
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
    # path("^login/$", SignupView.as_view(), name='account_signup'),
    # path('my-logout/', LogoutView.as_view(), name='account_logout'),
]


urlpatterns += (
    *[
        path(
            "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"
        ),
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="swagger-format",
        ),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    ],
    *[
        # path("admin/", admin.site.urls),
        # path("accounts/password/change/", UserLoginView.as_view(), name="admin-panel"),
        path("documents/", include(wagtaildocs_urls)),
        path("pages/", include(wagtail_urls)),
        re_path(
            r"^(?!static/|media/|api/|admin/|redoc/|swagger/).*",
            TemplateView.as_view(template_name="index.html"),
        ),
    ],
    *[
        path("accounts/", include("allauth.urls")),
        # path(
        #     "api/v1/dj-rest-auth/registration/account-confirm-email/<str:key>/",
        #     UserLoginView.as_view(),
        # ),
        # re_path("*", ),
    ],
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
