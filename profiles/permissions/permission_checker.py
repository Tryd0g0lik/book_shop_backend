# profiles/permissiona/permission_checker.py:1
from typing import Optional

from django.contrib.auth import get_user_model

from profiles.interfaces.interface_roles import UserProfile
from utilities.permissions import PermissionsMixin

Users = get_user_model()


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
    def can_view_to_profile(user: Optional[Users], user_owner: UserProfile) -> bool:
        user_owner = PermissionsChecker.is_owner(user, user_owner)
        is_moderator = PermissionsChecker.is_moderator(user)
        is_manager = PermissionsChecker.is_manager(user)
        is_admin = PermissionsChecker.is_admin(user)
        if user_owner or is_admin or is_manager or is_moderator:
            return True
        return False

    @staticmethod
    def can_edit_email_of_profile(user: Optional[Users]) -> bool:
        is_moderator = PermissionsChecker.is_moderator(user)
        is_admin = PermissionsChecker.is_admin(user)
        is_active = PermissionsChecker.is_active(user)
        if is_active and (is_moderator or is_admin):
            return True
        return False

    @staticmethod
    def can_adit_to_profile(user: Optional[Users], user_owner: UserProfile) -> bool:
        user_owner = PermissionsChecker.is_owner(user, user_owner)
        is_active = PermissionsChecker.is_active(user)
        is_manager = PermissionsChecker.is_manager(user)
        is_ = PermissionsChecker.can_edit_email_of_profile(user)

        if is_active and (user_owner or is_ or is_manager):
            return True
        return False

    @staticmethod
    def can_edit_profile_name(user: Optional[Users]) -> bool:
        is_admin = PermissionsChecker.is_admin(user)
        if is_admin:
            return True
        return False

    @staticmethod
    def can_delete_profile_name():
        return False

    @staticmethod
    def can_create_profile_name():
        return False
