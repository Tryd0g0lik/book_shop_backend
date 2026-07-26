# download/permissions/permission_drf.py:1

from rest_framework.permissions import BasePermission

from .permissions_checker import PermissionsChecker as _


class CanLoadFilePermission(BasePermission):
    """
    Here is we only loading the XLSX-file in aur server through an API-key,

    """

    def has_permission(self, request, view):
        return _.can_add_product(request.user)
