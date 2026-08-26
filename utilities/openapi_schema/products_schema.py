# utilities/openapi_schema/products_schema.py:1
from drf_yasg import openapi

from utilities.openapi_schema.brands_schema import (
    brand_request_schema,
    brand_response_schema,
)
from utilities.openapi_schema.categories_schema import (
    category_request_schema,
    category_response_schema,
)

SCHEMA_BASES_PROPERTIES = {
    "is_active": openapi.Schema(
        type=openapi.TYPE_BOOLEAN,
        description="Default value is a false.",
        example="false",
    ),
    "name": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Name of the product.",
        example="Ноутбук MacBook Air M2",
    ),
    "product_sku": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Product SKU - quantity of the product.",
        example="2",
    ),
    "price": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Price of the product.",
        format=openapi.FORMAT_DECIMAL,
        example="114990.00",
    ),
    "product_discount": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Discount of the product.",
        format=openapi.FORMAT_DECIMAL,
        example="0.00",
    ),
    "describe_preview": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Preview description of the product.",
        example="Тонкий и лёгкий с чипом M2",
    ),
    "description": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Full description of the product.",
        example='13.6" Liquid Retina, 8-core CPU, 10-core GPU, 256GB SSD',
    ),
    "discount_percent": openapi.Schema(
        type=openapi.TYPE_STRING,
        format=openapi.FORMAT_DECIMAL,
        description="Discount percent of the product.",
        example="5.00",
    ),
    "stock_quantity": openapi.Schema(
        type=openapi.TYPE_INTEGER,
        format=openapi.FORMAT_BASE64,
        example=30,
    ),
    "attributes_additional": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="THis block is attributes of properties  of the product.",
        example="""
            {
                'Год выпуска': '2023',
                ' цвет': ' серебристый'
            }
        """,
    ),
    "created_by": openapi.Schema(
        type=openapi.TYPE_INTEGER,
        format=openapi.FORMAT_INT64,
        description="This is an index of user which created the product.",
        example=1,
    ),
    "updated_by": openapi.Schema(
        type=openapi.TYPE_INTEGER,
        format=openapi.FORMAT_INT64,
        description="This is an index of user which updated the product.",
        example="null",
    ),
    "created_at": openapi.Schema(
        type=openapi.TYPE_STRING,
        format=openapi.FORMAT_DATETIME,
        description="It is a created time.",
        example="2026-08-02T15:34:00.829067+07:00",
    ),
    "updated_at": openapi.Schema(
        type=openapi.TYPE_STRING,
        format=openapi.FORMAT_DATETIME,
        description="It is a updating time.",
        example="2026-08-02T15:34:00.829067+07:00",
    ),
}

product_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, example=1
        ),
        **SCHEMA_BASES_PROPERTIES,
        "category": category_response_schema,
        "brand": brand_response_schema,
    },
)
product_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        **SCHEMA_BASES_PROPERTIES,
        "category": category_request_schema,
        "brand": brand_request_schema,
    },
)
