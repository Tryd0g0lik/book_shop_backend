# project/aurls_api.py:2
from django.urls import include, path, re_path

urlpatterns = [
    path(
        "persons/",
        include("persons.api_urls", namespace="persons_api"),
        name="persons_api",
    ),
]
