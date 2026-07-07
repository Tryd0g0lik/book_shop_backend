# # project/urls_api.py:2
from django.urls import include, path, re_path

from download.urls_api import urlpatterns as download_api

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
]
