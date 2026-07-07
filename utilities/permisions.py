from persons.interfaces import Users


class PermissionsMixin:

    @staticmethod
    def is_anonymous(user: Users) -> bool:
        return getattr(user, "is_anonymous")

    @staticmethod
    def is_authenticated(user: Users) -> bool:
        return getattr(user, "is_authenticated")

    @staticmethod
    def is_admin(user: Users) -> bool:
        return getattr(user, "is_superuser")

    @staticmethod
    def is_editor(user: Users) -> bool:
        group = getattr(user, "group")
        return group.name.lower() == "editors"

    @staticmethod
    def is_moderator(user: Users) -> bool:
        group = getattr(user, "group")
        return group.name.lower() == "moderators"

    @staticmethod
    def is_manager(user: Users) -> bool:
        group = getattr(user, "group")
        return group.name.lower() == "manager"

    @staticmethod
    def is_client(user: Users) -> bool:
        group = getattr(user, "group")
        return group.name.lower() == "client"

    @staticmethod
    def is_active(user: Users) -> bool:
        if getattr(user, "is_verified") and getattr(user, "is_active"):
            return True
        return False
