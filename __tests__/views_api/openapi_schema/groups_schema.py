# __tests__/tests_api/openapi_schema/groups_schema.py:1
from drf_yasg import openapi

group_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id":openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Group ID",
            example=1,
            format=openapi.FORMAT_INT64,
        ),
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Group name",
            enum=['Admin', 'Moderators', 'Editors', "Manager", "Client"],
            example="Moderators",
        )
    },
    required=["name"],
    additional_properties=True,
)
