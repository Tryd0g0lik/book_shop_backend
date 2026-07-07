# catalog/permissions/permissions_checker.py:1
from typing import Optional

from persons.interfaces import Users
from profiles.interfaces.interface_roles import UserProfile
from utilities.permissions import PermissionsMixin


class PermissionsChecker(PermissionsMixin):

    @staticmethod
    def is_owner(user: Optional[Users], user_owner: UserProfile) -> bool:
        user_owner = (
            getattr(user_owner, "user") if hasattr(user_owner, "user") else None
        )
        if user is not None and user_owner is not None:
            if PermissionsChecker.is_active(user_owner) and getattr(
                user, "id"
            ) == getattr(user_owner, "id"):
                return True
        return False

    @staticmethod
    def can_view_to_catalog():
        return True

    @staticmethod
    def can_view_to_product():
        return True

    @staticmethod
    def can_add_product(user: Optional[Users]) -> bool:
        is_active = PermissionsChecker.is_active(user)
        is_manager = PermissionsChecker.is_manager(user)
        is_editor = PermissionsChecker.is_editor(user)
        is_admin = PermissionsChecker.is_admin(user)
        is_moderator = PermissionsChecker.is_moderator(user)
        if is_active and (is_admin or is_manager or is_moderator or is_editor):
            return True
        return False

    @staticmethod
    def can_delete_product(user: Optional[Users], user_owner: UserProfile) -> bool:
        is_active = PermissionsChecker.is_active(user)
        is_admin = PermissionsChecker.is_admin(user)
        is_manager = PermissionsChecker.is_manager(user)
        is_editor = PermissionsChecker.is_editor(user)
        is_owner = PermissionsChecker.is_owner(user, user_owner)
        if PermissionsChecker.can_add_product(user, user_owner):
            if is_admin:
                return True
            elif is_active and (is_editor or is_manager) and is_owner:
                return True
        return False

    @staticmethod
    def can_edit_product(user: Optional[Users], user_owner: UserProfile) -> bool:
        if PermissionsChecker.can_add_product(user):
            return True
        return False
