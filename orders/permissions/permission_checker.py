# orders/permissions/permission_checker.py:1
from typing import Optional

from persons.interfaces import Users
from profiles.interfaces import UserProfileType
from utilities.permissions import PermissionsMixin


class PermissionsChecker(PermissionsMixin):
    @staticmethod
    def is_owner(user: Optional[Users], user_owner: UserProfileType) -> bool:
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
    def can_view_all_orders(user: Optional[Users]) -> bool:
        is_active = PermissionsChecker.is_active(user)
        is_moderator = PermissionsChecker.is_moderator(user)
        is_manager = PermissionsChecker.is_manager(user)
        is_admin = PermissionsChecker.is_admin(user)
        if is_active and is_moderator or is_manager or is_admin:
            return True
        return False

    @staticmethod
    def can_view_orders(user: Optional[Users], user_owner: UserProfileType) -> bool:
        is_active = PermissionsChecker.is_active(user)
        is_owner = PermissionsChecker.is_owner(user, user_owner)
        is_editor = PermissionsChecker.is_editor(user)
        is_client = PermissionsChecker.is_client(user)
        if not is_active:
            return False
        if PermissionsChecker.can_view_all_orders(user):
            return True
        if is_owner and is_editor or is_client:
            return True
        return False

    @staticmethod
    def can_delete_all_orders(user: Optional[Users]) -> bool:
        is_all_view = PermissionsChecker.can_view_all_orders(user)
        if is_all_view:
            return True
        return False

    @staticmethod
    def can_do_pay(user: Optional[Users], user_owner: UserProfileType) -> bool:
        is_active = PermissionsChecker.is_active(user)
        is_owner = PermissionsChecker.is_owner(user, user_owner)
        if is_active and is_owner:
            return True
        return False

    @staticmethod
    def can_edit_order() -> bool:
        return False
