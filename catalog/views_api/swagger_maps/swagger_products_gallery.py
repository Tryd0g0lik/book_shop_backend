# catalog/views_api/swagger_maps/swagger_products_gallery.py:1


from drf_yasg import openapi

from utilities.openapi_schema import image_response_schema, product_response_schema
from utilities.openapi_schema.products_schema import (
    SCHEMA_BASES_DATE,
    SCHEMA_BASES_PARAMETERS,
    SCHEMA_BASES_USERS,
)

acreate_mapping_product_gallery = {
    "describe_option": """
        Method: '`POST`'
        Pathname: '`/catalog/add/`'
        ============================================
        Note: It is update an one property or all properties together.
        Here is working with the model 'OneImageModels'.
        Any from the all properties (exclude 'id' of the line) that you can change.
        The creating of row allows user be at roles:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"
        ============================================
        This is an intermediate table between the "product page" table and "product properties" (itself product).
        It is a set of content for publish.
        Every item it is one page.
        Every page would be to contain the one product:
            1. The product, it is a page  that have a general content obout product
            2. The page contain a publish title and additional info.
            3. The images.

    """,
    "manual_parameters": [
        *SCHEMA_BASES_PARAMETERS,
        openapi.Schema(
            name="ID",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="The ID of line from the db",
            example="12",
            format=openapi.FORMAT_INT64,
        ),
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "caption": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The caption of the image",
                example="Test caption of catalog 2",
            ),
            "is_active": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Is active/publication or not",
                example="true",
            ),
            "product": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Product ID",
                format=openapi.FORMAT_INT64,
                example=981,
            ),
            "page": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Page ID",
                format=openapi.FORMAT_INT64,
                example=1,
            ),
        },
    ),
    "required": ["caption", "product", "page"],
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
                            "sort_order": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN, example="null"
                            ),
                            **SCHEMA_BASES_DATE,
                            "caption": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Test caption of catalog 3",
                            ),
                            "version": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                format=openapi.FORMAT_INT64,
                                example=1,
                            ),
                            "is_active": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN, example="true"
                            ),
                            "published_at": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_DATETIME,
                                description="This data create when 'is_active' getting the value 'true'.",
                                example="2026-08-28T14:13:10.666062+07:00",
                            ),
                            **SCHEMA_BASES_USERS,
                            "page": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER, example=1
                                    ),
                                    "product": product_response_schema,
                                    "image": image_response_schema,
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Test title"
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
                            # ---
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
                        "sort_order": "null",
                        "created_at": "2026-08-28T14:13:10.666557+07:00",
                        "updated_at": "2026-08-28T14:13:10.666591+07:00",
                        "caption": "Test caption of catalog 3",
                        "version": 1,
                        "is_active": "true",
                        "published_at": "2026-08-28T14:13:10.666062+07:00",
                        "created_by": 1,
                        "updated_by": "null",
                        "page": {
                            "id": 1,
                            "name": "Test name a prouct page",
                            "description": "null",
                            "created_at": "2026-08-27T11:01:39.205069+07:00",
                            "updated_at": "2026-08-27T11:01:39.205110+07:00",
                            "is_active": "true",
                        },
                        "product": {
                            "id": 982,
                            "created_at": "2026-08-10T08:59:03.392789+07:00",
                            "updated_at": "2026-08-10T08:59:03.392814+07:00",
                            "is_active": "true",
                            "name": "Наушники WH-1000XM5",
                            "product_sku": "3",
                            "price": "34990.00",
                            "product_discount": "0.00",
                            "describe_preview": "Шумоподавление премиум-класса",
                            "description": "Беспроводные, до 30 ч работы, быстрая зарядка",
                            "discount_percent": "15.00",
                            "stock_quantity": 120,
                            "attributes_additional": {
                                "Тип": " полноразмерные",
                                " Bluetooth": " 5.2",
                            },
                            "created_by": 1,
                            "updated_by": "null",
                            "category": {
                                "id": 3,
                                "name": "Наушники",
                                "description": "Аксессуары для звука",
                                "created_at": "2026-07-29T12:58:48.100988+07:00",
                                "updated_at": "2026-07-29T12:58:48.101020+07:00",
                            },
                            "brand": {
                                "id": 3,
                                "name": "Sony",
                                "description": "Японский бренд аудиотехники",
                                "created_at": "2026-07-29T12:58:48.009750+07:00",
                                "updated_at": "2026-07-29T12:58:48.009784+07:00",
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
aupdate_mapping_product_gallery = {
    "describe_option": """
        Method: '`PATCH`'
        Pathname: '`/catalog/add/`'
        ============================================
        Note: It is update an one property or all properties together.
        Here is working with the model 'OneImageModels'.
        Any from the all properties (exclude 'id' of the line) that you can change.
        The creating of row allows user be at roles:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"
        ============================================
        You can update the all or one property of single position.

    """,
    "manual_parameters": [
        *SCHEMA_BASES_PARAMETERS,
        openapi.Schema(
            name="ID",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="The ID of line from the db",
            example="12",
            format=openapi.FORMAT_INT64,
        ),
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "caption": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The caption of the image",
                example="Test caption of catalog 2",
            ),
            "is_active": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Is active/publication or not",
                example="true",
            ),
            "product": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Product ID",
                format=openapi.FORMAT_INT64,
                example=981,
            ),
            "page": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Page ID",
                format=openapi.FORMAT_INT64,
                example=1,
            ),
        },
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
                            "sort_order": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN, example="null"
                            ),
                            **SCHEMA_BASES_DATE,
                            "caption": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Test caption of catalog 3",
                            ),
                            "version": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                format=openapi.FORMAT_INT64,
                                example=1,
                            ),
                            "is_active": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN, example="true"
                            ),
                            "published_at": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_DATETIME,
                                description="This data create when 'is_active' getting the value 'true'.",
                                example="2026-08-28T14:13:10.666062+07:00",
                            ),
                            **SCHEMA_BASES_USERS,
                            "page": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER, example=1
                                    ),
                                    "product": product_response_schema,
                                    "image": image_response_schema,
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Test title"
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
                            # ---
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
                        "sort_order": "null",
                        "created_at": "2026-08-28T14:13:10.666557+07:00",
                        "updated_at": "2026-08-28T14:13:10.666591+07:00",
                        "caption": "Test caption of catalog 3",
                        "version": 1,
                        "is_active": "true",
                        "published_at": "2026-08-28T14:13:10.666062+07:00",
                        "created_by": 1,
                        "updated_by": "null",
                        "page": {
                            "id": 1,
                            "name": "Test name a prouct page",
                            "description": "null",
                            "created_at": "2026-08-27T11:01:39.205069+07:00",
                            "updated_at": "2026-08-27T11:01:39.205110+07:00",
                            "is_active": "true",
                        },
                        "product": {
                            "id": 982,
                            "created_at": "2026-08-10T08:59:03.392789+07:00",
                            "updated_at": "2026-08-10T08:59:03.392814+07:00",
                            "is_active": "true",
                            "name": "Наушники WH-1000XM5",
                            "product_sku": "3",
                            "price": "34990.00",
                            "product_discount": "0.00",
                            "describe_preview": "Шумоподавление премиум-класса",
                            "description": "Беспроводные, до 30 ч работы, быстрая зарядка",
                            "discount_percent": "15.00",
                            "stock_quantity": 120,
                            "attributes_additional": {
                                "Тип": " полноразмерные",
                                " Bluetooth": " 5.2",
                            },
                            "created_by": 1,
                            "updated_by": "null",
                            "category": {
                                "id": 3,
                                "name": "Наушники",
                                "description": "Аксессуары для звука",
                                "created_at": "2026-07-29T12:58:48.100988+07:00",
                                "updated_at": "2026-07-29T12:58:48.101020+07:00",
                            },
                            "brand": {
                                "id": 3,
                                "name": "Sony",
                                "description": "Японский бренд аудиотехники",
                                "created_at": "2026-07-29T12:58:48.009750+07:00",
                                "updated_at": "2026-07-29T12:58:48.009784+07:00",
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
adestroy_mapping_product_gallery = {
    "describe_option": """
        Method: '`DELETE`'
        Pathname: '`/catalog/delete/`'
        ============================================
        The delete of row allows user be at roles:
        - user.groups == "admin"
        - user.groups == "moderators"
        and below user can only hide from view (remove the publication) or delete if they are a author this positions.
        - user.groups == "editors"
        - user.groups == "manager"
        ============================================

    """,
    "manual_parameters": [
        openapi.Schema(
            name="ID",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="The ID of line from the db",
            example="12",
            format=openapi.FORMAT_INT64,
        ),
        *SCHEMA_BASES_PARAMETERS,
    ],
    "responses": {
        204: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="<TEXT-SUCCESSFULLY>",
                    )
                },
                required=["detail"],
            ),
            examples={
                "application/json": {
                    "detail": {
                        "id": 51,
                        "sort_order": "null",
                        "created_at": "2026-08-28T14:13:10.666557+07:00",
                        "updated_at": "2026-08-28T14:13:10.666591+07:00",
                        "caption": "Test caption of catalog 3",
                        "version": 1,
                        "is_active": "true",
                        "published_at": "2026-08-28T14:13:10.666062+07:00",
                        "created_by": 1,
                        "updated_by": "null",
                        "page": {
                            "id": 1,
                            "name": "Test name a prouct page",
                            "description": "null",
                            "created_at": "2026-08-27T11:01:39.205069+07:00",
                            "updated_at": "2026-08-27T11:01:39.205110+07:00",
                            "is_active": "true",
                        },
                        "product": {
                            "id": 982,
                            "created_at": "2026-08-10T08:59:03.392789+07:00",
                            "updated_at": "2026-08-10T08:59:03.392814+07:00",
                            "is_active": "true",
                            "name": "Наушники WH-1000XM5",
                            "product_sku": "3",
                            "price": "34990.00",
                            "product_discount": "0.00",
                            "describe_preview": "Шумоподавление премиум-класса",
                            "description": "Беспроводные, до 30 ч работы, быстрая зарядка",
                            "discount_percent": "15.00",
                            "stock_quantity": 120,
                            "attributes_additional": {
                                "Тип": " полноразмерные",
                                " Bluetooth": " 5.2",
                            },
                            "created_by": 1,
                            "updated_by": "null",
                            "category": {
                                "id": 3,
                                "name": "Наушники",
                                "description": "Аксессуары для звука",
                                "created_at": "2026-07-29T12:58:48.100988+07:00",
                                "updated_at": "2026-07-29T12:58:48.101020+07:00",
                            },
                            "brand": {
                                "id": 3,
                                "name": "Sony",
                                "description": "Японский бренд аудиотехники",
                                "created_at": "2026-07-29T12:58:48.009750+07:00",
                                "updated_at": "2026-07-29T12:58:48.009784+07:00",
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
aretrieve_mapping_product_gallery = {
    "describe_option": """
        Method: '`GET`'
        Pathname: '`/catalog/get/`'
        ============================================
        The look this position allow for users with roles:
        - all users.
        ============================================
    """,
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
                            "sort_order": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN, example="null"
                            ),
                            **SCHEMA_BASES_DATE,
                            "caption": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Test caption of catalog 3",
                            ),
                            "version": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                format=openapi.FORMAT_INT64,
                                example=1,
                            ),
                            "is_active": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN, example="true"
                            ),
                            "published_at": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_DATETIME,
                                description="This data create when 'is_active' getting the value 'true'.",
                                example="2026-08-28T14:13:10.666062+07:00",
                            ),
                            **SCHEMA_BASES_USERS,
                            "page": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER, example=1
                                    ),
                                    "product": product_response_schema,
                                    "image": image_response_schema,
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Test title"
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
                            # ---
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
                        "sort_order": "null",
                        "created_at": "2026-08-28T14:13:10.666557+07:00",
                        "updated_at": "2026-08-28T14:13:10.666591+07:00",
                        "caption": "Test caption of catalog 3",
                        "version": 1,
                        "is_active": "true",
                        "published_at": "2026-08-28T14:13:10.666062+07:00",
                        "created_by": 1,
                        "updated_by": "null",
                        "page": {
                            "id": 1,
                            "name": "Test name a prouct page",
                            "description": "null",
                            "created_at": "2026-08-27T11:01:39.205069+07:00",
                            "updated_at": "2026-08-27T11:01:39.205110+07:00",
                            "is_active": "true",
                        },
                        "product": {
                            "id": 982,
                            "created_at": "2026-08-10T08:59:03.392789+07:00",
                            "updated_at": "2026-08-10T08:59:03.392814+07:00",
                            "is_active": "true",
                            "name": "Наушники WH-1000XM5",
                            "product_sku": "3",
                            "price": "34990.00",
                            "product_discount": "0.00",
                            "describe_preview": "Шумоподавление премиум-класса",
                            "description": "Беспроводные, до 30 ч работы, быстрая зарядка",
                            "discount_percent": "15.00",
                            "stock_quantity": 120,
                            "attributes_additional": {
                                "Тип": " полноразмерные",
                                " Bluetooth": " 5.2",
                            },
                            "created_by": 1,
                            "updated_by": "null",
                            "category": {
                                "id": 3,
                                "name": "Наушники",
                                "description": "Аксессуары для звука",
                                "created_at": "2026-07-29T12:58:48.100988+07:00",
                                "updated_at": "2026-07-29T12:58:48.101020+07:00",
                            },
                            "brand": {
                                "id": 3,
                                "name": "Sony",
                                "description": "Японский бренд аудиотехники",
                                "created_at": "2026-07-29T12:58:48.009750+07:00",
                                "updated_at": "2026-07-29T12:58:48.009784+07:00",
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
alist_mapping_product_gallery = {
    "describe_option": """
        Method: '`GET`'
        Pathname: '`/catalog/get/`'
        ============================================
        The look this position allow for users with roles:
        - all users.
        ============================================
    """,
    "responses": {
        201: openapi.Response(
            description="Return the JSON byte-string. Key the 'detail'",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=1
                                ),
                                "sort_order": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN, example="null"
                                ),
                                **SCHEMA_BASES_DATE,
                                "caption": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Test caption of catalog 3",
                                ),
                                "version": openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    format=openapi.FORMAT_INT64,
                                    example=1,
                                ),
                                "is_active": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN, example="true"
                                ),
                                "published_at": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_DATETIME,
                                    description="This data create when 'is_active' getting the value 'true'.",
                                    example="2026-08-28T14:13:10.666062+07:00",
                                ),
                                **SCHEMA_BASES_USERS,
                                "page": openapi.Schema(
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
                                # ---
                            },
                        ),
                    )
                },
            ),
            examples={
                "application/json": {
                    "detail": [
                        {
                            "id": 51,
                            "sort_order": "null",
                            "created_at": "2026-08-28T14:13:10.666557+07:00",
                            "updated_at": "2026-08-28T14:13:10.666591+07:00",
                            "caption": "Test caption of catalog 3",
                            "version": 1,
                            "is_active": "true",
                            "published_at": "2026-08-28T14:13:10.666062+07:00",
                            "created_by": 1,
                            "updated_by": "null",
                            "page": {
                                "id": 1,
                                "name": "Test name a prouct page",
                                "description": "null",
                                "created_at": "2026-08-27T11:01:39.205069+07:00",
                                "updated_at": "2026-08-27T11:01:39.205110+07:00",
                                "is_active": "true",
                            },
                            "product": {
                                "id": 982,
                                "created_at": "2026-08-10T08:59:03.392789+07:00",
                                "updated_at": "2026-08-10T08:59:03.392814+07:00",
                                "is_active": "true",
                                "name": "Наушники WH-1000XM5",
                                "product_sku": "3",
                                "price": "34990.00",
                                "product_discount": "0.00",
                                "describe_preview": "Шумоподавление премиум-класса",
                                "description": "Беспроводные, до 30 ч работы, быстрая зарядка",
                                "discount_percent": "15.00",
                                "stock_quantity": 120,
                                "attributes_additional": {
                                    "Тип": " полноразмерные",
                                    " Bluetooth": " 5.2",
                                },
                                "created_by": 1,
                                "updated_by": "null",
                                "category": {
                                    "id": 3,
                                    "name": "Наушники",
                                    "description": "Аксессуары для звука",
                                    "created_at": "2026-07-29T12:58:48.100988+07:00",
                                    "updated_at": "2026-07-29T12:58:48.101020+07:00",
                                },
                                "brand": {
                                    "id": 3,
                                    "name": "Sony",
                                    "description": "Японский бренд аудиотехники",
                                    "created_at": "2026-07-29T12:58:48.009750+07:00",
                                    "updated_at": "2026-07-29T12:58:48.009784+07:00",
                                },
                            },
                        },
                    ]
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
