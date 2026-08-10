# catalog/views_api/view_one_image.py:1
from adrf import serializers
from adrf.viewsets import ModelViewSet
from django.apps import apps

from catalog.intarfaces import OneImageModelsType

OneImageModels: OneImageModelsType = apps.get_model("catalog", "OneImageModels")


class OneImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = OneImageModels
        fields = "__all__"


class OneImageViewSet(ModelViewSet):
    queryset = OneImageModels.objects.all()
    serializers_class = OneImageSerializers
