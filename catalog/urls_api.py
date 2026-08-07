# catalog/urls_api.py:1

from django.urls import path
from rest_framework import routers

from catalog.views import ProductViewSet

router = routers.DefaultRouter()
router.register("product", ProductViewSet)
urlpatterns = router.urls
