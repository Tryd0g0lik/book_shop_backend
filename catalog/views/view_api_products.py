# catalog/views/view_api_products.py:1
from typing import Any

from adrf import serializers
from adrf.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import ProductModel
from catalog.permissions.drf_permissions import DRFPermissionsChecker


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"


class ProductViewSet(ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DRFPermissionsChecker]
