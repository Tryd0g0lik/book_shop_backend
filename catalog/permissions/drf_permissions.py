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
        How make a call of a direct user from UserProfileManagerModel: 'persons.models.Users => wagtail.users.models.UserProfile =>
        profiles.models.model_<client | admin | editor | manager | client| moderator > => UserProfileManagerModel'
        """
        user = request.user
        if view.action == "list":
            return PermissionsChecker.can_view_to_catalog()
        elif view.action == "create":
            return PermissionsChecker.can_add_product(user)
        elif view.action in [
            "partial_update",
            "update",
        ]:
            return PermissionsChecker.can_edit_product(user)
        elif view.action == "destroy":
            return PermissionsChecker.can_delete_product(user)
        elif view.action in [
            "retrieve",
        ]:
            return True
        return False

    def has_object_permission(self, request: Request, view, obj):
        """
        Called single position. Check permissions that don't require a specific object.

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
            profile = user.groups.values_list("name", flat=True)[0]
            roles = [item[0].lower() for item in CATEGORY_STATUS]

            if profile.lower() in roles:
                return True

            return False
        except Exception as e:
            log.error(e.args[0])
            return False
