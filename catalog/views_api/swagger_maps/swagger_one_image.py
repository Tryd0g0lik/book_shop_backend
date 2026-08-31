# catalog/views_api/swagger_maps/swagger_one_image.py:1
# Apply to the  catalog/views_api/view_one_image.py
from drf_yasg import openapi

from utilities.openapi_schema import (
    image_response_schema,
    product_response_schema,
    user_schema,
)

acreate_mapping = {
    "operation_description": """
        Method: '`POST`'
        Pathname: '`/catalog/image/`'
        ============================================
        **THis image for the product page**
        This is a method use permissions of the user's role.
        It does not upload the image file from the user local dick. Here we is choosing an one image from the server.
        Chosen by us this image it is for publication to the web page of product.
        Thanks to this we can  choice one or some images.
        The creating of row allows user be at roles:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"

        Note: Before choosing an image you will should be to upload this image in to the server.
        """,
    "tags": ["catalog_image"],
    "operation_summary": """
                The working properties: 'title', 'describe', "label", "x", "y", 'image_id', 'product_id'.
            """,
    "manual_parameters": [
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
            description="JWT-tokens the 'access' & 'update'",
            required=True,
        ),
        openapi.Schema(
            name="user",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_OBJECT,
            schema=user_schema,
        ),
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Data for the one product image and uploads/connection image from the server.",
        properties={
            "count": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                format=openapi.FORMAT_INT64,
                example=20,
            ),
            "next": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                example="http://127.0.0.1:8000/api/catalog/product/get/?limit=3&offset=3",
            ),
            "previous": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                example="http://127.0.0.1:8000/api/catalog/product/get/?page=2&page_size=3",
            ),
            "result": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "product": product_response_schema,
                        "image": image_response_schema,
                        "title": openapi.Schema(
                            type=openapi.TYPE_STRING, example="Test title"
                        ),
                        "describe": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Test description",
                        ),
                        "x": openapi.Schema(type=openapi.TYPE_NUMBER, example=12.0),
                        "y": openapi.Schema(type=openapi.TYPE_NUMBER, example=12.0),
                    },
                ),
            ),
        },
        required=[
            "product_id",
            "image_id",
            "title",
        ],
        additional_properties=False,
    ),
    "responses": {
        200: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "product": product_response_schema,
                            "image": image_response_schema,
                            "title": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Test title"
                            ),
                            "describe": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Test description"
                            ),
                            "x": openapi.Schema(type=openapi.TYPE_NUMBER, example=12.0),
                            "y": openapi.Schema(type=openapi.TYPE_NUMBER, example=12.0),
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
                            "focal_point_x": "null",
                            "focal_point_y": "null",
                            "focal_point_width": "null",
                            "focal_point_height": "null",
                            "file_size": 282252,
                            "uploaded_by_user": 1,
                        },
                        "product": {
                            "id": 981,
                            "created_at": "2026-08-10T08:59:03.137733+07:00",
                            "updated_at": "2026-08-10T08:59:03.137764+07:00",
                            "is_active": "true",
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
                                " цвет": " серебристый",
                            },
                            "created_by": 1,
                            "updated_by": "null",
                            "category": {
                                "id": 2,
                                "name": "Ноутбуки",
                                "description": "Портативные компьютеры для работы и творчества",
                                "created_at": "2026-07-29T12:58:47.534138+07:00",
                                "updated_at": "2026-07-29T12:58:47.534168+07:00",
                            },
                            "brand": {
                                "id": 2,
                                "name": "Apple",
                                "description": "Американская компания, лидер в инновациях",
                                "created_at": "2026-07-29T12:58:47.459462+07:00",
                                "updated_at": "2026-07-29T12:58:47.459491+07:00",
                            },
                        },
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
}

# ---
partial_aupdate_mappping = {
    "openation_description": """
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
    "operation_summary": """
                The working properties: 'title', 'describe', "label", "x", "y", 'image_id', 'product_id'.
            """,
    "tags": ["catalog_image"],
    "methods": ["patch"],
    "manual_parameters": [
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
            description="JWT-tokens the 'access' & 'update'",
            required=True,
        ),
        openapi.Schema(
            name="user",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_OBJECT,
            schema=user_schema,
        ),
    ],
    "request_body": openapi.Schema(
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
    "responses": {
        200: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "count": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                format=openapi.FORMAT_INT64,
                                example=20,
                            ),
                            "next": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                example="http://127.0.0.1:8000/api/catalog/product/get/?limit=3&offset=3",
                            ),
                            "previous": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                example="http://127.0.0.1:8000/api/catalog/product/get/?page=2&page_size=3",
                            ),
                            "result": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(
                                            type=openapi.TYPE_INTEGER, example=1
                                        ),
                                        "product": product_response_schema,
                                        "image": image_response_schema,
                                        "title": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            example="Test title",
                                        ),
                                        "describe": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            example="Test description",
                                        ),
                                        "x": openapi.Schema(
                                            type=openapi.TYPE_NUMBER, example=12.0
                                        ),
                                        "y": openapi.Schema(
                                            type=openapi.TYPE_NUMBER, example=12.0
                                        ),
                                    },
                                ),
                            ),
                        },
                    )
                },
                required=["detail"],
            ),
            examples={
                "application/json": {
                    "detail": {
                        "count": 20,
                        "next": "http://127.0.0.1:8000/api/catalog/product/get/?limit=3&offset=3",
                        "previous": "null",
                        "results": [
                            {
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
                                    "focal_point_x": "null",
                                    "focal_point_y": "null",
                                    "focal_point_width": "null",
                                    "focal_point_height": "null",
                                    "file_size": 282252,
                                    "uploaded_by_user": 1,
                                },
                                "product": {
                                    "id": 981,
                                    "created_at": "2026-08-10T08:59:03.137733+07:00",
                                    "updated_at": "2026-08-10T08:59:03.137764+07:00",
                                    "is_active": "true",
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
                                        " цвет": " серебристый",
                                    },
                                    "created_by": 1,
                                    "updated_by": "null",
                                    "category": {
                                        "id": 2,
                                        "name": "Ноутбуки",
                                        "description": "Портативные компьютеры для работы и творчества",
                                        "created_at": "2026-07-29T12:58:47.534138+07:00",
                                        "updated_at": "2026-07-29T12:58:47.534168+07:00",
                                    },
                                    "brand": {
                                        "id": 2,
                                        "name": "Apple",
                                        "description": "Американская компания, лидер в инновациях",
                                        "created_at": "2026-07-29T12:58:47.459462+07:00",
                                        "updated_at": "2026-07-29T12:58:47.459491+07:00",
                                    },
                                },
                            }
                        ],
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
}
alist_mappping = {
    "openation_description": """
        Method: '`GET`'
        Pathname: '`/catalog/image/'
        ============================================
        Note: It is get a list images.
        Here is working with the model 'OneImageModels'.
        The get list of rows allows, if the user is in one from role:
        - all users
        """,
    "operation_summary": """
                The working properties: 'title', 'describe', "label", "x", "y", 'image_id', 'product_id'.
            """,
    "tags": ["catalog_image"],
    "methods": ["get"],
    "responses": {
        200: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "count": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                format=openapi.FORMAT_INT64,
                                example=20,
                            ),
                            "next": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                example="http://127.0.0.1:8000/api/catalog/product/get/?limit=3&offset=3",
                            ),
                            "previous": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                example="http://127.0.0.1:8000/api/catalog/product/get/?page=2&page_size=3",
                            ),
                            "results": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(
                                            type=openapi.TYPE_INTEGER, example=1
                                        ),
                                        "product": product_response_schema,
                                        "image": image_response_schema,
                                        "title": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            example="Test title",
                                        ),
                                        "describe": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            example="Test description",
                                        ),
                                        "x": openapi.Schema(
                                            type=openapi.TYPE_NUMBER, example=12.0
                                        ),
                                        "y": openapi.Schema(
                                            type=openapi.TYPE_NUMBER, example=12.0
                                        ),
                                    },
                                ),
                            ),
                        },
                    )
                },
                required=["detail"],
            ),
            examples={
                "application/json": {
                    "detail": {
                        "count": 20,
                        "next": "http://127.0.0.1:8000/api/catalog/product/get/?limit=3&offset=3",
                        "previous": "null",
                        "results": [
                            {
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
                                    "focal_point_x": "null",
                                    "focal_point_y": "null",
                                    "focal_point_width": "null",
                                    "focal_point_height": "null",
                                    "file_size": 282252,
                                    "uploaded_by_user": 1,
                                },
                                "product": {
                                    "id": 981,
                                    "created_at": "2026-08-10T08:59:03.137733+07:00",
                                    "updated_at": "2026-08-10T08:59:03.137764+07:00",
                                    "is_active": "true",
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
                                        " цвет": " серебристый",
                                    },
                                    "created_by": 1,
                                    "updated_by": "null",
                                    "category": {
                                        "id": 2,
                                        "name": "Ноутбуки",
                                        "description": "Портативные компьютеры для работы и творчества",
                                        "created_at": "2026-07-29T12:58:47.534138+07:00",
                                        "updated_at": "2026-07-29T12:58:47.534168+07:00",
                                    },
                                    "brand": {
                                        "id": 2,
                                        "name": "Apple",
                                        "description": "Американская компания, лидер в инновациях",
                                        "created_at": "2026-07-29T12:58:47.459462+07:00",
                                        "updated_at": "2026-07-29T12:58:47.459491+07:00",
                                    },
                                },
                            }
                        ],
                    }
                }
            },
        ),
        404: openapi.Response(
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
}
aretrive_mappping = {
    "openation_description": """
        Method: '`GET`'
        Pathname: '`/catalog/<int:pk>/image/'
        ============================================
        Note: It is get a list images.
        Here is working with the model 'OneImageModels'.
        The get list of rows allows, if the user is in one from role:
        - all users
        """,
    "operation_summary": """
                The working properties: 'title', 'describe', "label", "x", "y", 'image_id', 'product_id'.
            """,
    "tags": ["catalog_image"],
    "methods": ["get"],
    "responses": {
        200: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "product": product_response_schema,
                            "image": image_response_schema,
                            "title": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Test title",
                            ),
                            "describe": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Test description",
                            ),
                            "x": openapi.Schema(type=openapi.TYPE_NUMBER, example=12.0),
                            "y": openapi.Schema(type=openapi.TYPE_NUMBER, example=12.0),
                        },
                    )
                },
                required=["detail"],
            ),
            examples={
                "application/json": {
                    "detail": {
                        "count": 20,
                        "next": "http://127.0.0.1:8000/api/catalog/product/get/?limit=3&offset=3",
                        "previous": "null",
                        "results": [
                            {
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
                                    "focal_point_x": "null",
                                    "focal_point_y": "null",
                                    "focal_point_width": "null",
                                    "focal_point_height": "null",
                                    "file_size": 282252,
                                    "uploaded_by_user": 1,
                                },
                                "product": {
                                    "id": 981,
                                    "created_at": "2026-08-10T08:59:03.137733+07:00",
                                    "updated_at": "2026-08-10T08:59:03.137764+07:00",
                                    "is_active": "true",
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
                                        " цвет": " серебристый",
                                    },
                                    "created_by": 1,
                                    "updated_by": "null",
                                    "category": {
                                        "id": 2,
                                        "name": "Ноутбуки",
                                        "description": "Портативные компьютеры для работы и творчества",
                                        "created_at": "2026-07-29T12:58:47.534138+07:00",
                                        "updated_at": "2026-07-29T12:58:47.534168+07:00",
                                    },
                                    "brand": {
                                        "id": 2,
                                        "name": "Apple",
                                        "description": "Американская компания, лидер в инновациях",
                                        "created_at": "2026-07-29T12:58:47.459462+07:00",
                                        "updated_at": "2026-07-29T12:58:47.459491+07:00",
                                    },
                                },
                            }
                        ],
                    }
                }
            },
        ),
        404: openapi.Response(
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
}
# ---
adestroy_mapping = {
    "methods": ["delete"],
    "tags": ["catalog_image"],
    "manual_parameters": [
        openapi.Parameter(
            name="Authorization",
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description="JWT-tokens the 'access' & 'update'",
            required=True,
        ),
        openapi.Schema(
            name="user",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_OBJECT,
            schema=user_schema,
        ),
    ],
    "responses": {
        204: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING, examples="All successfully!"
                    )
                },
                required=["detail"],
            ),
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
}
