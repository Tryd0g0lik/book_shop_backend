# cart/permissions/permission_checker.py:1
from django.contrib.auth import get_user_model
from shtab import Optional

from persons import CATEGORY_STATUS
from persons.interfaces import Users as Persons
from profiles.interfaces import (
    AdminProfileModel,
    ClientProfileModel,
    EditorProfileModel,
    ManagerProfileModel,
    ModeratorProfileModel,
)

Users = get_user_model()
# -- Roles


class PermissionsChecker:
    def __new__(cls, *args, **kwargs):
        initial = super().__new__(*args, **kwargs)
        initial.roles = [list(item)[0] for item in CATEGORY_STATUS]
        return initial

    @staticmethod
    def is_anonymous(user: Users) -> bool:
        return user.is_anonymous

    @staticmethod
    def is_authenticated(user: Users) -> bool:
        return user.is_authenticated

    @staticmethod
    def is_admin(user: Users) -> bool:
        return user.is_superuser

    @staticmethod
    def is_active(user: Users) -> bool:
        if user.is_verified and user.is_active:
            return True
        return False

    @staticmethod
    def can_add_to_card(
        user: Optional[Users],
        cart_owner: Optional[
            ClientProfileModel
            | AdminProfileModel
            | ModeratorProfileModel
            | ManagerProfileModel
            | EditorProfileModel
        ],
    ) -> bool:
        """Everyone user can add to cart"""
        if user is not None:
            if user.is_anonymous:
                return True
            if PermissionsChecker.is_active(user) and cart_owner is not None:
                user.group.name == cart_owner.user.group.name

        return True

    @staticmethod
    def can_edit_cart() -> bool:
        """Everyone user can edit cart"""
        return True

    @staticmethod
    def can_delete_cart() -> bool:
        """Everyone user can delete cart"""
        return True
