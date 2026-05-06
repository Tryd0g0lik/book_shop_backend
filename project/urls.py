"""
URL configuration for backend backend.

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

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from persons.views import UserLoginView, UsersRegistrationView
from project import settings
from project.settings import LOGIN_URL

urlpatterns = [
    # path("admin/", admin.site.urls),
    re_path("register/", UsersRegistrationView.as_view(), name="register"),
    re_path("login/", UserLoginView.as_view(), name="login"),
]
urlpatterns += [path("accounts/", include("mailauth.urls"))]
urlpatterns += [
    # path("admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls), name="admin-panel"),
    path("documents/", include(wagtaildocs_urls)),
    path("pages/", include(wagtail_urls)),
    re_path(
        r"^(?!static/|media/|api/|admin/|redoc/|swagger/).*",
        TemplateView.as_view(template_name="index.html"),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
