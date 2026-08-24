# catalog/views_api/view_one_image.py:1
import asyncio
import json
import logging

from adrf.requests import Request
from adrf.viewsets import ModelViewSet
from django.apps import apps
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from __tests__.tests_api.openapi_schema.users_schema import user_schema
from catalog.intarfaces import OneImageModelsType, ProductModelType
from catalog.serializers import OneImageSerializers

OneImageModels: OneImageModelsType = apps.get_model("catalog", "OneImageModels")
ProductModel: ProductModelType = apps.get_model("catalog", "ProductModel")
ImageModel = apps.get_model("wagtailimages", "Image")

log = logging.getLogger(__name__)


class OneImageViewSet(ModelViewSet):
    queryset = OneImageModels.objects.all()
    serializer_class = OneImageSerializers
    permission_classes = [IsAdminUser]
    LOCK = asyncio.Lock()

    PREFIX_LOG = "[OneImageViewSet]"

    @swagger_auto_schema(method_post=["post"], auto_schema=None)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="""
        Method: '`POST`'
        Pathname: '`/catalog/image/custom-create/`'
        ============================================
        **THis image for the product page**
        This is a method for use permissions of the user's roles.
        It does not upload the image file from the user local dick. Here we choice an one image from the server.
        Chosen by us this image it is for publication to the web page of product.
        Thanks to this we can  choice one or some images.
        The upload of file (xls) allows user to be:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"

        Note: Before choosing an image you will should be to upload this image in to the server.
        """,
        tags=["catalog", "image"],
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
                type=openapi.TYPE_INTEGER,
                example=12,
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
                                "product": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=12
                                ),
                                "image": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=2
                                ),
                                "title": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Test title"
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
                            "describe": "",
                            "title": "Test_title_2026_08_23_12_17_54_08s",
                            "x": 0,
                            "y": 0,
                            "id": 1,
                            "product": 1,
                            "image": 1,
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
        serialize, product_obj, image_obj = None, None, None
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.create.__name__)
        try:
            self.check_permissions(request)
        except Exception as e:
            error_t = "{} User Id: {} He does not have permission! {}".format(
                prefix_log, str(request.user.id), e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        product_id = data.get("product_id")
        image_id = data.get("image_id")
        try:
            # ============================================
            # GETTING DEPENDENTS MODELS
            # ============================================
            product_obj = await ProductModel.objects.aget(id=product_id)
            image_obj, created = await ImageModel.objects.aget_or_create(id=image_id)
        except ModuleNotFoundError as e:
            error_t = "{} ModuleNotFoundError => {}".format(
                prefix_log, e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_400_BAD_REQUEST)
        except (ProductModel.DoesNotExist, ImageModel.DoesNotExist) as e:
            error_t = "{} DoesNotExist => {}".format(
                prefix_log, e.args[0] if e.args else str(e)
            )
            log.error(error_t)
            return JsonResponse({"detail": error_t}, status=status.HTTP_400_BAD_REQUEST)
        try:
            del data["product_id"], data["image_id"]
            data.__setitem__("product", product_obj.id)
            data.__setitem__("image", image_obj.id)

            try:
                serialize = OneImageSerializers(data=data)
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
            # ============================================
            # CHECKING A DATA VALIDATION
            # ============================================
            # is_valid = await asyncio.to_thread(lambda: serialize.is_valid())
            is_valid = await asyncio.to_thread(serialize.is_valid)
            if is_valid:
                await serialize.asave()

                resource = JsonResponse(
                    {"detail": serialize.data}, status=status.HTTP_200_OK
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
