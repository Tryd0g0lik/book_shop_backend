# # project/urls_api.py:2
from django.urls import include, path, re_path

from download.urls_api import urlpatterns as download_api

urlpatterns = [
    path(
        "download/",
        include(download_api),
    ),
]
