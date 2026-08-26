# catalog/views_api/view_one_image.py:1
import asyncio
import logging

from django.apps import apps
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from adrf.requests import Request
from adrf.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from utilities.openapi_schema import product_response_schema
from utilities.openapi_schema.images_schema import image_response_schema
from utilities.openapi_schema.users_schema import user_schema

from catalog.intarfaces import (OneImageModelsType, ProductModelType)
from catalog.serializers import OneImageSerializers

OneImageModels: OneImageModelsType = apps.get_model("catalog", "OneImageModels")
ProductModel: ProductModelType = apps.get_model("catalog", "ProductModel")
ImageModel = apps.get_model("wagtailimages", "Image")

log = logging.getLogger(__name__)


class ProductImageViewSet(ModelViewSet):
    queryset = OneImageModels.objects.select_related(
        "image",
        "product"
    ).all()
    serializer_class = OneImageSerializers
    permission_classes = [IsAdminUser]

    PREFIX_LOG = "[ProductImageViewSet]"


    @swagger_auto_schema(auto_schema=None, tags=["free"])
    def create(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(auto_schema=None, tags=["free"])
    def update(self, request: Request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(auto_schema=None, tags=["free"])
    def partial_update(self, request: Request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(auto_schema=None, tags=["free"], )
    def destroy(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(auto_schema=None, tags=["free"], )
    def list(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(auto_schema=None, tags=["free"], )
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        operation_description="""
        Method: '`POST`'
        Pathname: '`/catalog/image/`'
        ============================================
        **THis image for the product page**
        This is a method for use permissions of the user's roles.
        It does not upload the image file from the user local dick. Here we choice an one image from the server.
        Chosen by us this image it is for publication to the web page of product.
        Thanks to this we can  choice one or some images.
        The creating of row allows user be at roles:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"
        
        Note: Before choosing an image you will should be to upload this image in to the server.
        """,
        tags=["image"],
        operation_summary="""
            The working properties: 'title', 'describe', "label", "x", "y", 'image_id', 'product_id'. 
        """,
        manual_parameters=[
            openapi.Parameter(
                name="Content-Type",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="application/json",
                required=True,
            ),
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="JWT-tokens the 'access' & 'update'" ,
                required=True,
            ),
            openapi.Schema(
                name="user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_OBJECT,
                schema=user_schema,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="Data for the one product image and uploads/connection image from the server.",
            properties={
                "product_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_INT64,
                    description="The id of the product.",
                    example=12,
                ),
                "image_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="The id of the product image.",
                    format=openapi.FORMAT_INT64,
                    example=2,
                ),
                "describe": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The description of the image.",
                    example="This is the description of the image.",
                ),
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The title of the image.",
                    example="This is the title of the image.",
                ),
                "x": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_FLOAT,
                    description="The x coordinate of the image.",
                    example=12.0,
                ),
                "y": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_FLOAT,
                    description="The y coordinate of the image.",
                    example=12.0,
                ),
            },
            required=[
                "product_id",
                "image_id",
                "title",
            ],
            additional_properties=False,
        ),
        responses={
            200: openapi.Response(
                description="Return the JSON byte-string. Key the 'detail'",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=1
                                ),
                                "product":  product_response_schema,
                                "image": image_response_schema,
                                "title": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Test title"
                                ),
                                "describe": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Test description"
                                ),
                                "x": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, example=12.0
                                ),
                                "y": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, example=12.0
                                ),
                            },
                            required=["id", "product", "image", "title"],
                        )
                    },
                    required=["detail"],
                ),
                examples={
                    "application/json": {
                        "detail": {
                            "id": 51,
                            "title": "Test_title_cheged",
                            "describe": "",
                            "label": "label",
                            "x": "11.00",
                            "y": "10.00",
                            "image": {
                                "id": 1,
                                "title": "Form_of-registration",
                                "file": "/media/original_images/Form_of-registration.png",
                                "description": "Описание Test image 1",
                                "width": 1463,
                                "height": 764,
                                "created_at": "2026-08-02T15:34:00.829067+07:00",
                                "focal_point_x": 'null',
                                "focal_point_y": 'null',
                                "focal_point_width": 'null',
                                "focal_point_height": 'null',
                                "file_size": 282252,
                                "uploaded_by_user": 1
                            },
                            "product": {
                                "id": 981,
                                "created_at": "2026-08-10T08:59:03.137733+07:00",
                                "updated_at": "2026-08-10T08:59:03.137764+07:00",
                                "is_active": 'true',
                                "name": "Ноутбук MacBook Air M2",
                                "product_sku": "2",
                                "price": "114990.00",
                                "product_discount": "0.00",
                                "describe_preview": "Тонкий и лёгкий с чипом M2",
                                "description": "13.6 Liquid Retina, 8-core CPU, 10-core GPU, 256GB SSD",
                                "discount_percent": "5.00",
                                "stock_quantity": 30,
                                "attributes_additional": {
                                    "Год выпуска": " 2023",
                                    " цвет": " серебристый"
                                },
                                "created_by": 1,
                                "updated_by": 'null',
                                "category": {
                                    "id": 2,
                                    "name": "Ноутбуки",
                                    "description": "Портативные компьютеры для работы и творчества",
                                    "created_at": "2026-07-29T12:58:47.534138+07:00",
                                    "updated_at": "2026-07-29T12:58:47.534168+07:00"
                                },
                                "brand": {
                                    "id": 2,
                                    "name": "Apple",
                                    "description": "Американская компания, лидер в инновациях",
                                    "created_at": "2026-07-29T12:58:47.459462+07:00",
                                    "updated_at": "2026-07-29T12:58:47.459491+07:00"
                                }
                            }
                        }
                    }
                },
            ),
            400: openapi.Response(
                description="<ERROR FROM DATA or SERIALISE or REQUEST>",
                examples={"application/json": {"detail": "< TEXT-ERROR >"}},
            ),
            403: openapi.Response(
                description="Permission denied",
                examples={"application/json": {"detail": "< TEXT-ERROR>"}},
            ),
            500: openapi.Response(
                description="Error",
                examples={"application/json": {"detail": "< TEXT-ERROR>"}},
            ),
        },

    )
    @action(detail=False, methods=["post"])
    async def acreate(self, request: Request, *args, **kwargs):
        """
        TODO Dec-commenting the permissions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serialize, product_obj, image_obj = None, None, None
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.acreate.__name__)
        try:
            self.check_permissions(request)
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
            # del data["product_id"], data["image_id"]
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
            log.debug("DEBUG {} \nSerialize={} ".format(prefix_log, str(serialize),))
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
                resource = JsonResponse(
                    {"detail": data}, status=status.HTTP_200_OK
                )
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


    @swagger_auto_schema(
        openation_description="""
        Method: '`PATCH`'
        Pathname: '`/catalog/image/<Index_of_line>/'
        ============================================
        Note: It is update an one property or all properties together.  
        Here is working with the model 'OneImageModels'. 
        Any from the all properties (exclude 'id' of the line) that you can change.
        The creating of row allows user be at roles:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"
        
        Note: Before choosing an image you will should be to upload this image in to the server.
        """,
        operation_summary="""
            The working properties: 'title', 'describe', "label", "x", "y", 'image_id', 'product_id'. 
        """,
        tags=["image"],
        methods=["patch"],
        manual_parameters=[
            openapi.Parameter(
                name="Content-Type",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="application/json",
                required=True,
            ),
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="JWT-tokens the 'access' & 'update'" ,
                required=True,
            ),
            openapi.Schema(
                name="user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_OBJECT,
                schema=user_schema,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="Data for the one product image and uploads/connection image from the server.",
            properties={
                "product_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_INT64,
                    description="The id of the product.",
                    example=12,
                ),
                "image_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="The id of the product image.",
                    format=openapi.FORMAT_INT64,
                    example=2,
                ),
                "describe": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The description of the image.",
                    example="This is the description of the image.",
                ),
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The title of the image.",
                    example="This is the title of the image.",
                ),
                "x": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_FLOAT,
                    description="The x coordinate of the image.",
                    example=12.0,
                ),
                "y": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    format=openapi.FORMAT_FLOAT,
                    description="The y coordinate of the image.",
                    example=12.0,
                ),
            },
            additional_properties=False,
        ),
        responses={
            200: openapi.Response(
                description="Return the JSON byte-string. Key the 'detail'",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=1
                                ),
                                "product":  product_response_schema,
                                "image": image_response_schema,
                                "title": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Test title"
                                ),
                                "describe": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Test description"
                                ),
                                "x": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, example=12.0
                                ),
                                "y": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, example=12.0
                                ),
                            },
                        )
                    },
                    required=["detail"],
                ),
                examples={
                    "application/json": {
                        "detail": {
                            "id": 51,
                            "title": "Test_title_cheged",
                            "describe": "",
                            "label": "label",
                            "x": "11.00",
                            "y": "10.00",
                            "image": {
                                "id": 1,
                                "title": "Form_of-registration",
                                "file": "/media/original_images/Form_of-registration.png",
                                "description": "Описание Test image 1",
                                "width": 1463,
                                "height": 764,
                                "created_at": "2026-08-02T15:34:00.829067+07:00",
                                "focal_point_x": 'null',
                                "focal_point_y": 'null',
                                "focal_point_width": 'null',
                                "focal_point_height": 'null',
                                "file_size": 282252,
                                "uploaded_by_user": 1
                            },
                            "product": {
                                "id": 981,
                                "created_at": "2026-08-10T08:59:03.137733+07:00",
                                "updated_at": "2026-08-10T08:59:03.137764+07:00",
                                "is_active": 'true',
                                "name": "Ноутбук MacBook Air M2",
                                "product_sku": "2",
                                "price": "114990.00",
                                "product_discount": "0.00",
                                "describe_preview": "Тонкий и лёгкий с чипом M2",
                                "description": "13.6 Liquid Retina, 8-core CPU, 10-core GPU, 256GB SSD",
                                "discount_percent": "5.00",
                                "stock_quantity": 30,
                                "attributes_additional": {
                                    "Год выпуска": " 2023",
                                    " цвет": " серебристый"
                                },
                                "created_by": 1,
                                "updated_by": 'null',
                                "category": {
                                    "id": 2,
                                    "name": "Ноутбуки",
                                    "description": "Портативные компьютеры для работы и творчества",
                                    "created_at": "2026-07-29T12:58:47.534138+07:00",
                                    "updated_at": "2026-07-29T12:58:47.534168+07:00"
                                },
                                "brand": {
                                    "id": 2,
                                    "name": "Apple",
                                    "description": "Американская компания, лидер в инновациях",
                                    "created_at": "2026-07-29T12:58:47.459462+07:00",
                                    "updated_at": "2026-07-29T12:58:47.459491+07:00"
                                }
                            }
                        }
                    }
                },
            ),
            400: openapi.Response(
                description="<ERROR FROM DATA or SERIALISE or REQUEST>",
                examples={"application/json": {"detail": "< TEXT-ERROR >"}},
            ),
            403: openapi.Response(
                description="Permission denied",
                examples={"application/json": {"detail": "< TEXT-ERROR>"}},
            ),
            500: openapi.Response(
                description="Error",
                examples={"application/json": {"detail": "< TEXT-ERROR>"}},
            ),
        },

    )
    @action(detail=True, methods=["patch"], url_path="update")
    async def partial_aupdate(self,  request: Request, *args, **kwargs):
        serialize = None
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.partial_aupdate.__name__)
        data = request.data
        try:
            self.check_permissions(request)
        except Exception as e:
            error_t = "{} User Id: {} He does not have permission! {}".format(
                prefix_log, str(request.user.id), e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_403_FORBIDDEN)
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
            error_t = "{} ERROR => {}".format(prefix_log, e.args[0] if e.args else str(e))
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        methods=["get"],
        tags=["image"],
    )
    @action(detail=False, methods=["get"], url_path="get")
    async def alist(self, *args, **kwargs):
        return await super().alist(*args, **kwargs)

    @swagger_auto_schema(
        methods=["get"],
        tags=["image"],
    )
    @action(detail=True, methods=["get"], url_path="get")
    async def aretrieve(self, *args, **kwargs):
        return await super().aretrieve(*args, **kwargs)
    @swagger_auto_schema(
            methods=["delete"],
            tags=["image"],
        )
    @action(detail=True, methods=["delete"], url_path="remove")
    async def adestroy(self, *args, **kwargs):
        return await super().adestroy(*args, **kwargs)

    def _get_wgt_image_raw(self, image_id) -> ImageModel:
        log_t = "{}[{}]:".format(self.PREFIX_LOG, self._get_wgt_image_raw.__name__)
        image_query = ImageModel.objects.raw("""
        SELECT * 
            FROM wagtailimages_image wi
            INNER JOIN person p
            ON wi.uploaded_by_user_id = p.id
            INNER JOIN wagtailcore_collection wc
            ON wi.collection_id = wc.id
            WHERE wi.id = %s
            LIMIT 1;
        """, [str(image_id)])
        image_obj = list(image_query)[0] if image_query and len(list(image_query)) > 0 else None
        if image_obj is None:
            raise ImageModel.DoesNotExist("{} Image id: {} not found".format(log_t,image_id))
        return image_obj


