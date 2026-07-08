# # project/urls_api.py:2
from django.urls import include, path, re_path

# from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from download.urls_api import urlpatterns as download_api
from persons.views.serializers.token_obtain_serializer import TokenObtainPairSerializer

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(
        "download/",
        include(download_api),
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
