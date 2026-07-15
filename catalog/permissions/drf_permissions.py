# catalog/permissions/drf_permissions.py:1
import logging

from django.db.models import Q, QuerySet
from pandas import isnull
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from persons.tasks.tasks_celery.task_create_position.functions import (
    get_fields_of_model,
)
from profiles.exceptions.error_profile import ProfileNotFound
from profiles.models import UserProfileManagerModel
from utilities import CATEGORY_STATUS

from ..exceptions import ProductValueError
from .permissions_checker import PermissionsChecker

log = logging.getLogger(__name__)


class DRFPermissionsChecker(BasePermission):
    """
    DRF-compatible permission class that wraps for PermissionsChecker logic

    """

    def has_permission(self, request: Request, view):
        """
        Called for all requests. Check permissions that don't require a specific object.
        """
        user = request.user
        if view.action == "list":
            return PermissionsChecker.can_view_to_catalog()
        elif view.action == "create":
            return PermissionsChecker.can_add_product(user)
        elif view.action in ["retrieve", "partial_update", "update", "destroy"]:
            return True
        return False

    def has_object_permission(self, request: Request, view, obj):
        """
        Called for all requests. Check permissions that don't require a specific object.
        How make a call of a direct user from UserProfileModel: 'persons.models.Users => wagtail.users.models.UserProfile =>
        profiles.models.model_<client | admin | editor | manager | client| moderator > => UserProfileModel'
        :param request:
        :param view:
        :param obj:
        :return:
        """
        log_t = "[{}][{}]:".format(
            DRFPermissionsChecker.__class__.__name__,
            self.has_object_permission.__name__,
        )
        user = request.user
        try:
            if user.is_anonymous:
                raise ProductValueError(
                    "{} ERROR => The user is AnonymousUser".format(log_t)
                )
            # ============================================
            # DEFINING A USER's PROFILE FROM REQUEST
            # dict(zip(range(0, len(res_list) ), res_list))
            # ============================================
            user_group_names: QuerySet = user.groups.values_list("name", flat=True)

            user_group_name = user_group_names[0] if user_group_names else None
            profile_names = get_fields_of_model(UserProfileManagerModel)

            # Check the fields "updated_by" & "created_by" - this is an exists or not
            obj_updated_by = (
                hasattr(obj, "updated_by") if hasattr(obj, "updated_by") else None
            )
            obj_created_by = (
                hasattr(obj, "created_by") if hasattr(obj, "created_by") else None
            )
            if obj_created_by is None and obj_updated_by is None:
                raise ProductValueError(
                    "{} ERROR => The 'obj' hase not properties: 'updated_by' or 'created_by'".format(
                        log_t
                    )
                )
            profile_verify: dict = {
                item: Q(**{f"{item}__isnull": False})
                for item in profile_names
                if item != "id"
            }
            # ============================================
            # DEFINING a USER's PROFILE OF the OWNER FROM of the 'obj'
            # Here we have 'obj' (from catalog) and us are needing to get the index of the own user. That is user
            # which created this 'obj'.
            # ============================================
            owner_profile_queryset = UserProfileManagerModel.objects.filter(
                profile_verify.get(user_group_name.lower(), Q())
            )

            if not owner_profile_queryset.exists():
                raise ProductValueError(
                    "{} ERROR => The fields, that define/contain of the owner ( of the 'obj') not bound".format(
                        log_t
                    )
                )
            owner_profile_queryset = (
                owner_profile_queryset.filter(Q(updated_by=obj_updated_by))
                if obj_updated_by is not None
                else owner_profile_queryset.filter(Q(created_by=obj_created_by))
            )
            # Search a field that does not have a null value
            if not owner_profile_queryset.exists():
                raise ProductValueError(
                    "{} ERROR => The 'updated_by' & 'created_by' properties are set None".format(
                        log_t
                    )
                )

            profile_of_own_user: UserProfileManagerModel = (
                owner_profile_queryset.first()
            )
            non_null_field = None
            for field_name in profile_names:
                field_value = getattr(profile_of_own_user, field_name, None)
                if field_value is not None:
                    non_null_field = field_name
                    break
            if non_null_field is None:
                raise ProductValueError(
                    "{} Did not find the field that does not have a null value!".format(
                        log_t
                    )
                )
            # We are getting an index of the named profile of the user.
            # This the named profile contain the 'user' of a Wagtail's field.
            profile_id = getattr(profile_of_own_user, non_null_field, None)
            # ПРО-ВЕ-РИТЬ !!!!
            profile_obj = owner_profile_queryset.get(
                Q(**{f"{non_null_field}__profile_{non_null_field}__id": profile_id})
            )
            profile_wagtail_obj = profile_obj.objects.filter(
                Q(user__user_id__isnull=False)
            )
            if profile_wagtail_obj.exists() is None:
                raise ProductValueError(
                    "{} Wagtail's profile of user does not find!".format(log_t)
                )
            profile_wagtail = profile_wagtail_obj.first()
            own_user = profile_wagtail.user_id
            if view.action == "retrieve":
                return PermissionsChecker.can_view_to_product()
            elif view.action in ["update", "partial_update"]:
                # For PUT/PATCH request (update)
                return PermissionsChecker.can_edit_product(user, own_user)
            elif view.action == "destroy":
                # For DELETE request (destroy)
                return PermissionsChecker.can_delete_product(user, own_user)

            return False
        except Exception as e:
            log.error(e.args[0])
            return False
