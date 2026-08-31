# catalog/views_api/swagger_maps/swagger_product_pages.py:1
# Use to to the 'ProductPageViewSet'
from drf_yasg import openapi

from utilities.openapi_schema.products_schema import (
    SCHEMA_BASES_DATE,
    SCHEMA_BASES_PARAMETERS,
)

acreate_mappings_product_page = {
    "operation_description": """
            Method: '`POST`'
            Pathname: '`api/catalog/page/add/`'
            ============================================
            Note: Users who can create a new line in database.
            Here is working with the model 'ProductPageModel'.
            User's roles:
            - user.groups == "admin"
            - user.groups == "moderators"
            - user.groups == "editors"
            - user.groups == "manager"

            ============================================
        """,
    "manual_parameters": [
        *SCHEMA_BASES_PARAMETERS,
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Unique name of page",
                example="Test name a product page",
            ),
            "is_active": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Is this page active? Default value is False",
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Description of page. Default value is None",
            ),
        },
        required=["name"],
        responses={
            "detail": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        format=openapi.FORMAT_INT64,
                        example=1,
                    ),
                    "name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Unique name of page",
                        example="Test name a product page",
                    ),
                    "is_active": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Is this page active? Default value is False",
                    ),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Description of page. Default value is None",
                    ),
                    **SCHEMA_BASES_DATE,
                },
            ),
        },
    ),
    "responses": {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            format=openapi.FORMAT_INT64,
                            example=1,
                        ),
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique name of page",
                        ),
                        "is_active": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="If '`is_active=True'`",
                            example=True,
                        ),
                        **SCHEMA_BASES_DATE,
                    },
                )
            },
        ),
        403: "You have no permission to perform this action.",
        500: "Internal Server Error",
    },
    "example": """
            {
                "detail": {
                    "id": 4,
                    "name": "Test name a product page 1",
                    "description": null,
                    "created_at": "2026-08-31T13:37:50.769197+07:00",
                    "updated_at": "2026-08-31T14:10:54.099758+07:00",
                    "is_active": true
                }
            }
        """,
}
alist_mappings_product_page = {
    "operation_description": """
            Method: '`GET`'
            Pathname: '`api/catalog/page/get/`'
            ============================================
            Note: Users who can be reading data.
            Here is working with the model 'ProductPageModel'.
            Users can be at roles (They are reading):
            - user.groups == "admin"
            - user.groups == "moderators"
            - user.groups == "editors"
            - user.groups == "manager"
            - user.groups == "Anonymous"
            - user.groups == "Client"
            - user.groups == "Basis"

            ============================================
        """,
    "responses": {
        200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                format=openapi.FORMAT_INT64,
                                example=1,
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Unique name of page",
                            ),
                            "is_active": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description="If '`is_active=True'`",
                                example=True,
                            ),
                            **SCHEMA_BASES_DATE,
                        },
                    )
                },
            ),
        ),
        403: "You have no permission to perform this action.",
        500: "Internal Server Error",
    },
    "example": """
            {
                "detail": [{
                    "id": 4,
                    "name": "Test name a product page 1",
                    "description": null,
                    "created_at": "2026-08-31T13:37:50.769197+07:00",
                    "updated_at": "2026-08-31T14:10:54.099758+07:00",
                    "is_active": true
                },]
            }
        """,
}

aretrieve_mappings_product_page = {
    "operation_description": """
            Method: '`GET`'
            Pathname: '`api/catalog/page/<int:id>/get/`'
            ============================================
            Note: Users who can be reading data.
            Here is working with the model 'ProductPageModel'.
            Users can be at roles (They are reading):
            - user.groups == "admin"
            - user.groups == "moderators"
            - user.groups == "editors"
            - user.groups == "manager"
            - user.groups == "Anonymous"
            - user.groups == "Client"
            - user.groups == "Basis"

            ============================================
        """,
    "responses": {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            format=openapi.FORMAT_INT64,
                            example=1,
                        ),
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique name of page",
                        ),
                        "is_active": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="If '`is_active=True'`",
                            example=True,
                        ),
                        **SCHEMA_BASES_DATE,
                    },
                )
            },
        ),
        403: "You have no permission to perform this action.",
        500: "Internal Server Error",
    },
    "example": """
            {
                "detail": {
                    "id": 4,
                    "name": "Test name a product page 1",
                    "description": null,
                    "created_at": "2026-08-31T13:37:50.769197+07:00",
                    "updated_at": "2026-08-31T14:10:54.099758+07:00",
                    "is_active": true
                },
            }
        """,
}
aupdate_mappings_product_page = {
    "operation_description": """
                Method: '`UPDATE`'
                Pathname: '`api/catalog/page/<int:id>/update/`'
                ============================================
                Note: Users who can update a line in database.
                Here is working with the model 'ProductPageModel'.
                User's roles:
                - user.groups == "admin"
                - user.groups == "moderators"
                - user.groups == "editors"
                - user.groups == "manager"

                ============================================
            """,
    "manual_parameters": [
        *SCHEMA_BASES_PARAMETERS,
    ],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Unique updated name of page",
            ),
            "is_active": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Updated values.",
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Updated description",
            ),
        },
        responses={
            "detail": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        format=openapi.FORMAT_INT64,
                        example=1,
                    ),
                    "name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Unique updated name of page",
                    ),
                    "is_active": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Updated values.",
                    ),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Updated description",
                    ),
                    **SCHEMA_BASES_DATE,
                },
            ),
        },
    ),
    "responses": {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            format=openapi.FORMAT_INT64,
                            example=1,
                        ),
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique updated name of page",
                        ),
                        "is_active": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="Updated values.",
                        ),
                        "description": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Updated description",
                        ),
                        **SCHEMA_BASES_DATE,
                    },
                )
            },
        ),
        403: "You have no permission to perform this action.",
        500: "Internal Server Error",
    },
    "example": """
                {
                    "detail": {
                        "id": 4,
                        "name": "Test updated name a product page 1",
                        "description": < updated description>,
                        "created_at": "2026-08-31T13:37:50.769197+07:00",
                        "updated_at": "2026-08-31T14:10:54.099758+07:00",
                        "is_active":  < updated description>,
                    }
                }
            """,
}
adestroy_mappings_product_page = {
    "operation_description": """
            Method: '`DELETE`'
            Pathname: '`api/catalog/page/delete/`'
            ============================================
            Note: Users who can remove a line from database.
            Here is working with the model 'ProductPageModel'.
            User's roles:
            - user.groups == "admin"
            - user.groups == "moderators"
            - user.groups == "editors"
            - user.groups == "manager"

            ============================================
        """,
    "manual_parameters": [
        *SCHEMA_BASES_PARAMETERS,
    ],
    "responses": {
        204: "Not found.",
        403: "You have no permission to perform this action.",
        500: "Internal Server Error",
    },
}
