# catalog/views_api/view_one_image.py:1
import asyncio
import logging
from typing import Optional

from adrf.requests import Request
from adrf.viewsets import ModelViewSet
from django.apps import apps
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import action

from catalog.intarfaces import OneImageModelsType, ProductModelType
from catalog.permissions.permissions_checker import PermissionsChecker
from catalog.serializers_catalog import OneImageSerializers
from catalog.views_api.swagger_maps.swagger_one_image import (
    acreate_mapping,
    adestroy_mapping,
    alist_mappping,
    aretrive_mappping,
    partial_aupdate_mappping,
)

OneImageModels: OneImageModelsType = apps.get_model("catalog", "OneImageModels")
ProductModel: ProductModelType = apps.get_model("catalog", "ProductModel")
ImageModel = apps.get_model("wagtailimages", "Image")

log = logging.getLogger(__name__)


class ProductImageViewSet(ModelViewSet):
    queryset = OneImageModels.objects.select_related("image", "product").all()
    serializer_class = OneImageSerializers
    PREFIX_LOG = "[ProductImageViewSet]"


    @swagger_auto_schema(**acreate_mapping)
    @action(detail=False, methods=["post"])
    async def acreate(self, request: Request, *args, **kwargs):
        """
        TODO Dec-commenting the permissions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serialize, image_obj = None, None
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.acreate.__name__)
        self.check_permissions(request)

        try:
            result_bool = await asyncio.to_thread(lambda : PermissionsChecker().can_add_product(request.user))
            if not result_bool:
                raise
        except Exception as e:
            error_t = "{} User Id: {} He does not have permission! {}".format(
                prefix_log, str(request.user.id), e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_403_FORBIDDEN)
        # Beginning collection data
        data = request.data
        product_id = data.pop("product_id")
        image_id = data.pop("image_id")

        try:
            data.__setitem__("product", product_id)
            data.__setitem__("image", image_id)
            try:
                serialize = OneImageSerializers(data=data)
            except TypeError as e:
                error_t = "{} TypeError => {}".format(prefix_log, e.args[0])
                log.error(error_t)
                return JsonResponse(
                    {"detail": error_t}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            log.debug(
                "DEBUG {} \nSerialize={} ".format(
                    prefix_log,
                    str(serialize),
                )
            )
            if serialize is None:
                return JsonResponse(
                    {"detail": "The serialise is invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # ============================================
            # CHECKING A DATA VALIDATION
            # Sending data to the front.
            # ============================================
            is_valid = await asyncio.to_thread(serialize.is_valid)
            if is_valid:
                await serialize.asave()
                data = await serialize.adata
                resource = JsonResponse({"detail": data}, status=status.HTTP_200_OK)
                return resource
            response = JsonResponse(
                {"detail": "Data not valid!"}, status=status.HTTP_400_BAD_REQUEST
            )
            return response
        except Exception as e:
            error_t = "{} Error => {}".format(
                prefix_log, list(e.args)[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse(
                {"detail": error_t},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    @swagger_auto_schema(**partial_aupdate_mappping)
    @action(detail=True, methods=["patch"], url_path="update")
    async def partial_aupdate(self, request: Request, *args, **kwargs):
        serialize = None
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.partial_aupdate.__name__)
        try:
            result_bool = await asyncio.to_thread(lambda : PermissionsChecker().can_edit_product(request.user))
            if not result_bool:
                raise
        except Exception as e:
            error_t = "{} User Id: {} He does not have permission! {}".format(
                prefix_log, str(request.user.id), e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_403_FORBIDDEN)
        data = request.data

        try:
            try:
                instace = await self.aget_object()
                serialize = OneImageSerializers(instace, data=data, partial=True)
            except TypeError as e:
                error_t = "{} TypeError => {}".format(prefix_log, e.args[0])
                log.error(error_t)
                return JsonResponse(
                    {"detail": error_t}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if serialize is None:
                return JsonResponse(
                    {"detail": "The serialise is invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            is_valid = await asyncio.to_thread(serialize.is_valid)
            if is_valid:
                await serialize.asave()
                data = await serialize.adata
                resource = JsonResponse({"detail": data}, status=status.HTTP_200_OK)
                return resource
            response = JsonResponse(
                {"detail": "Data not valid!"}, status=status.HTTP_400_BAD_REQUEST
            )
            return response
        except Exception as e:
            error_t = "{} ERROR => {}".format(
                prefix_log, e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse(
                {"detail": error_t}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(**alist_mappping)
    @action(detail=False, methods=["get"], url_path="get")
    async def alist(self, *args, **kwargs):
        response = await super().alist(*args, **kwargs)
        return JsonResponse({"detail": response.data}, status=response.status_code)

    @swagger_auto_schema(**aretrive_mappping)
    @action(detail=True, methods=["get"], url_path="get")
    async def aretrieve(self, *args, **kwargs):
        response = await super().aretrieve(*args, **kwargs)
        return JsonResponse({"detail": response.data}, status=response.status_code)


    @swagger_auto_schema(**adestroy_mapping)
    @action(detail=True, methods=["delete"], url_path="remove")
    async def adestroy(self, request, *args, **kwargs):
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.adestroy.__name__)
        try:
            result_bool = await asyncio.to_thread(lambda : PermissionsChecker().can_edit_product(request.user))
            if not result_bool:
                raise
        except Exception as e:
            error_t = "{} User Id: {} He does not have permission! {}".format(
                prefix_log, str(request.user.id), e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_403_FORBIDDEN)
        response = await super().adestroy(*args, **kwargs)
        return JsonResponse({"detail": response.data}, status=response.status_code)

    # ---
    @swagger_auto_schema(auto_schema=None, tags=["free"])
    def create(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(auto_schema=None, tags=["free"])
    def update(self, request: Request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(auto_schema=None, tags=["free"])
    def partial_update(self, request: Request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        auto_schema=None,
        tags=["free"],
    )
    def destroy(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        auto_schema=None,
        tags=["free"],
    )
    def list(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        auto_schema=None,
        tags=["free"],
    )
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
