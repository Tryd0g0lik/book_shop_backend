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

from persons.urls import urlpatterns as persons_urls
from project import settings
from project.settings_conf.settings_env import APP_NAME

# from .urls_api import urlpatterns as hub_urls

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
    patterns=[
        # path("api/", include(("project.urls_api", "hub_api"), namespace="hub_api")),
    ],
)

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("api/", include("project.urls_api")),
    path("admin/", include(wagtailadmin_urls), name="admin-panel"),
    path("", include(persons_urls), name="persons_urls"),
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
