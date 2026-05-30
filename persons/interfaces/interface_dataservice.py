from typing import TYPE_CHECKING, Optional, Protocol

from .interface_persons import UsersPydantic

if TYPE_CHECKING:
    from persons.models import Users


class PersonService(Protocol):

    @staticmethod
    def get_user_by_id(user_id: Optional[int] = None) -> Optional[UsersPydantic]: ...

    @staticmethod
    def get_user_by_email(
        user_email: Optional[str] = None,
    ) -> Optional[UsersPydantic]: ...

    @staticmethod
    def search_by_email(user_email: str) -> list[UsersPydantic]: ...

    @staticmethod
    def is_email(user_email: str) -> bool: ...

    @staticmethod
    def is_password(user_data: dict) -> bool: ...

    @staticmethod
    def create_or_update_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
    ) -> "Users": ...
