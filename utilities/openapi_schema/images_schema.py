# utilities/openapi_schema/images_schema.py:1
# It is the Wagtail's Image Schema
from drf_yasg import openapi

SCHEMA_BASES_PROPERTIES = {
    "title": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="It is a title/header.",
        example="Form_of-registration",
    ),
    "file": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="It is a path name to a file.",
        example="/media/original_images/Form_of-registration.png",
    ),
    "description": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="It is a description of file which will be publication.",
        example="Описание Test image 1",
    ),
    "width": openapi.Schema(
        type=openapi.TYPE_INTEGER, description="It is a width of file.", example=1463
    ),
    "height": openapi.Schema(
        type=openapi.TYPE_INTEGER, description="It is a height of file.", example=764
    ),
    "created_at": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="It is a created time.",
        example="2026-08-02T15:34:00.829067+07:00",
    ),
    "focal_point_x": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_FLOAT, example="null"
    ),
    "focal_point_y": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_FLOAT, example="null"
    ),
    "focal_point_width": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_FLOAT, example="null"
    ),
    "focal_point_height": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_FLOAT, example="null"
    ),
    "file_size": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, example=282252
    ),
    "uploaded_by_user": openapi.Schema(
        type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, example=1
    ),
}
image_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, example=1
        ),
        **SCHEMA_BASES_PROPERTIES,
    },
)
image_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT, properties={**SCHEMA_BASES_PROPERTIES}
)
