# catalog/urls_api.py:1

from django.urls import path
from rest_framework import routers

from catalog.views_api import OneImageViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register("product", ProductViewSet)
router.register("image", OneImageViewSet)
urlpatterns = router.urls
