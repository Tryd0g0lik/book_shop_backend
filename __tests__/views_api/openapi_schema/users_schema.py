# __tests__/tests_api/openapi_schema/users_schema.py:1
# Note Important: This file is working and to the descript swagger's map-schem (to the '<APP_NAME.views.view_<FILE_NAME>.py>')!!!
from drf_yasg import openapi

from __tests__.tests_api.openapi_schema.groups_schema import group_schema

user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id":openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="User ID",
            format=openapi.FORMAT_INT64,
            example=2,
        ),
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Username/login",
            example="Moderator_38",
        ),
        "is_superuser": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Is superuser or non",
            example=True,
        ),
        "is_anonymous": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Is anonymous",
            example=True,
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Email address",
            example="admin@example.com",
            format=openapi.FORMAT_EMAIL,
        ),
        "is_staff": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="He has a staff or non ",
            example=True,
        ),
        "groups": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="User group",
            items=group_schema,
            require=True
        ),
        "is_active": openapi.Schema(
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_BOOLEAN,
            description="Is active ot not",
            example=True,
        ),

    },
    required=["is_superuser", "is_anonymous", "is_staff", "is_active", "groups"],
    additional_properties=True
)
