# catalog/views_api/view_api_products.py:1
from adrf import serializers
from adrf.viewsets import ModelViewSet

from catalog.models import ProductModel
from catalog.permissions.permissions_drf import DRFPermissionsChecker


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"


class ProductViewSet(ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DRFPermissionsChecker]

