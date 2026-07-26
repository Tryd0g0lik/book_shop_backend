from typing import Optional

from persons.interfaces import Users


class PermissionsMixin:
    @staticmethod
    def is_active(user: Optional[Users]) -> bool:
        if user is None:
            return False
        elif getattr(user, "is_verified") and getattr(user, "is_active"):
            return True
        return False

    @staticmethod
    def is_anonymous(user: Optional[Users]) -> bool:
        return hasattr(user, "is_anonymous")

    @staticmethod
    def is_authenticated(user: Optional[Users]) -> bool:
        return hasattr(user, "is_authenticated") and getattr(user, "is_authenticated")

    @staticmethod
    def is_admin(user: Optional[Users]) -> bool:

        return hasattr(user, "is_superuser") and bool(getattr(user, "is_superuser"))

    @staticmethod
    def is_editor(user: Users) -> bool:
        group = getattr(user, "groups")
        return isinstance(group.name, str) and group.name.lower() == "editors"

    @staticmethod
    def is_moderator(user: Users) -> bool:
        group = getattr(user, "groups")
        return isinstance(group.name, str) and group.name.lower() == "moderators"

    @staticmethod
    def is_manager(user: Users) -> bool:
        group = getattr(user, "groups")
        return isinstance(group.name, str) and group.name.lower() == "manager"

    @staticmethod
    def is_client(user: Users) -> bool:
        group = getattr(user, "groups")
        return isinstance(group.name, str) and group.name.lower() == "client"
