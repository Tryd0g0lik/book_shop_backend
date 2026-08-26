# utilities/openapi_schema/brands_schema.py:1

from drf_yasg import openapi

SCHEMA_BASES_PROPERTIES = {
    "name": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Brand of the product.",
        example="Apple",
    ),
    "description": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Describe of brand of the product.",
        example="Американская компания, лидер в инновациях",
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
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, example=2
    ),
    **SCHEMA_BASES_PROPERTIES,
}

brand_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT, properties=SCHEMA_RESPONSE_PROPERTIES
)
brand_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT, properties=SCHEMA_BASES_PROPERTIES
)
