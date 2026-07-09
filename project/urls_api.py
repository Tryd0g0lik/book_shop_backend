# # project/urls_api.py:2
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from download.urls_api import urlpatterns as download_api

urlpatterns = [
    path(
        "download/",
        include(download_api),
    ),
    path(
        "catalog/",
        include(("catalog.urls_api", "catalog"), namespace="catalog_api"),
        name="catalog_api",
    ),
    path(
        "orders/",
        include(("orders.urls_api", "orders"), namespace="orders_api"),
        name="orders_api",
    ),
    # JWT TOKENS
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
