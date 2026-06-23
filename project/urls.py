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

from allauth.urls import urlpatterns as allauth_urls

# Редирект с /admin/login/ на страницу входа allauth
# re_path(r'^admin/login/$', lambda request: redirect('/accounts/login/?next=/admin/')),
# Редирект с внутреннего URL Wagtail
# path('_util/login/', lambda request: redirect('/accounts/login/')),
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.admin.views import account, home
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from persons.urls import urlpatterns as persons_urls
from persons.views import UserLoginView
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
    re_path(r"^sitemap\.xml$", sitemap),
    path(
        "person/",
        include((persons_urls, "persons"), namespace="persons"),
        name="persons",
    ),
    re_path("admin/login/", UserLoginView.as_view(), name="wagtailadmin_login"),
    re_path(r"^admin/", include(wagtailadmin_urls)),
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
        path("accounts/", include("allauth.urls")),
    ],
    *[
        path("documents/", include(wagtaildocs_urls)),
        path("pages/", include(wagtail_urls)),
        # re_path(
        #     r"^(?!static/|media/|api/|redoc/|swagger/).*",
        #     TemplateView.as_view(template_name="index.html"),
        # ),
    ],
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
