import logging
from typing import Optional

from persons.interfaces import Users

log = logging.getLogger(__name__)


class PermissionsMixin:
    @staticmethod
    def is_active(user: Optional[Users]) -> bool:
        try:
            if user is None:
                return False
            elif getattr(user, "is_verified") and getattr(user, "is_active"):
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def is_anonymous(user: Optional[Users]) -> bool:
        try:
            return hasattr(user, "is_anonymous")
        except Exception:
            return False

    @staticmethod
    def is_authenticated(user: Optional[Users]) -> bool:
        try:
            return hasattr(user, "is_authenticated") and getattr(
                user, "is_authenticated"
            )
        except Exception:
            return False

    @staticmethod
    def is_admin(user: Optional[Users]) -> bool:
        try:
            return hasattr(user, "is_superuser") and getattr(user, "is_superuser")
        except Exception:
            return False

    @staticmethod
    def is_editor(user: Users) -> bool:
        try:
            group = getattr(user, "groups")
            first = group.first()
            result_bool = (
                isinstance(first.name, str)
                and first.name.lower() == "editors"
                and user.is_staff
            )
            return result_bool

        except Exception:
            return False

    @staticmethod
    def is_moderator(user: Users) -> bool:
        try:
            group = getattr(user, "groups")
            first = group.first()
            result_bool = (
                isinstance(first.name, str)
                and first.name.lower() == "moderators"
                and user.is_staff
            )
            return result_bool
        except Exception:
            return False

    @staticmethod
    def is_manager(user: Users) -> bool:
        try:
            group = getattr(user, "groups")
            first = group.first()
            return (
                isinstance(first.name, str)
                and first.name.lower() == "manager"
                and user.is_staff
            )
        except Exception:
            return False

    @staticmethod
    def is_client(user: Users) -> bool:
        try:
            group = getattr(user, "groups")
            first = group.first()
            return isinstance(first.name, str) and first.name.lower() == "client"
        except Exception:
            return False
