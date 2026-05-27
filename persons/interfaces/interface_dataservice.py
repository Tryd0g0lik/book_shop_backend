from typing import Optional

from .interface_persons import UsersPydantic


class PersonServiceInitialize:

    @staticmethod
    def get_user_by_id(user_id: Optional[int] = None) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        pass

    @staticmethod
    def get_user_by_email(
        user_email: Optional[str] = None,
    ) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        pass

    @staticmethod
    def search_by_email(user_email: str) -> list[UsersPydantic]:
        """Search users by email"""
        pass

    @staticmethod
    def is_email(user_email: str) -> bool:
        """Search users by email"""
        pass

    @staticmethod
    def is_password(user_data: dict) -> bool:
        """Search users by email"""
        pass

    @staticmethod
    def create_or_update_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
    ) -> UsersPydantic:
        """
        Args:
            :param user_data: Dictionary with fields to update
            :param user_id: User ID (optional)
            :param user_email: User email (optional)

        Returns:
            Updated user as Pydantic model
        """
        pass
