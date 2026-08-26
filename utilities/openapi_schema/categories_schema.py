# utilities/openapi_schema/categories_schema.py:1
from drf_yasg import openapi

SCHEMA_BASES_PROPERTIES = {
    "name": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Name of category of the product.",
        example="Ноутбуки",
    ),
    "description": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Describe of category of the product.",
        example="Портативные компьютеры для работы и творчества",
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
SCHEMA_RESPONSE_PROPERTIES = {
    "id": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, example=1
    ),
    **SCHEMA_BASES_PROPERTIES,
}
category_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT, properties=SCHEMA_RESPONSE_PROPERTIES
)
category_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT, properties=SCHEMA_BASES_PROPERTIES
)
