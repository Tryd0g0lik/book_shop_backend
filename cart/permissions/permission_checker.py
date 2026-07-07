# cart/permissions/permission_checker.py:1
from typing import Optional

from django.contrib.auth import get_user_model

from profiles.interfaces.interface_roles import UserProfile
from utilities.permissions import PermissionsMixin

Users = get_user_model()
# -- Roles


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
    def can_add_to_card(
        user: Optional[Users],
        cart_owner: UserProfile,
    ) -> bool:
        """Everyone user can add to cart"""
        user_owner = (
            getattr(cart_owner, "user") if hasattr(cart_owner, "user") else None
        )
        if user is not None:
            if PermissionsChecker.is_anonymous(user):
                return True
            elif PermissionsChecker.is_owner(user, user_owner):
                return True
        return False

    @staticmethod
    def can_edit_to_cart(user: Users, cart_owner: UserProfile) -> bool:
        result_bool = PermissionsChecker.can_add_to_card(user, cart_owner)
        if result_bool or (
            PermissionsChecker.is_admin(user) and PermissionsChecker.is_active(user)
        ):
            return True
        return False

    @staticmethod
    def can_delete_to_cart(user: Users, cart_owner: UserProfile) -> bool:
        if PermissionsChecker.can_edit_to_cart(user, cart_owner):
            return True
        elif (
            PermissionsChecker.is_admin(user)
            or PermissionsChecker.is_manager(user)
            or PermissionsChecker.is_moderator(user)
        ):
            return True
        return False

    @staticmethod
    def can_view_to_cart(user: Users, cart_owner: UserProfile) -> bool:
        if PermissionsChecker.can_delete_to_cart(user, cart_owner):
            return True
        return False
