# catalog/permissions/drf_permissions.py:1
from typing import Optional

from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from persons.interfaces import Users
from profiles.models import UserProfileModel

from .permissions_checker import PermissionsChecker


class DRFPermissionsChecker(BasePermission):
    """
    DRF-compatible permission class that wraps for PermissionsChecker logic
    """

    def has_permission(self, request: Request, view):
        """
        Called for all requests. Chck permissions that don't require a specific object.
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
        user = request.user
        own_user: Optional[Users] = None
        profile_queryset = UserProfileModel.objects.filter(
            Q(product__isnull=False) and Q(product=obj.id) and Q(user=user)
        )
        if profile_queryset.exists():
            own_user = profile_queryset.first()
        if view.action == "retrieve":
            return PermissionsChecker.can_view_to_product()
        elif view.action == ["update", "partial_update"]:
            # For PUT/PATCH request (update)
            return PermissionsChecker.can_edit_product(user, own_user)
        elif view.action == "destroy":
            # For DELETE request (destroy)
            return PermissionsChecker.can_delete_product(user, own_user)

        return False
