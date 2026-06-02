# persons/interfaces/interface_postman.py:2
import asyncio
from typing import ClassVar, Optional, Protocol

from persons.exceptions import PersonErrorImproperlyConfigured
from persons.exceptions.error_postman import PostmanRequiredModelError
from persons.interfaces import UsersPydantic


class PersonBasisMixin(Protocol):
    def __init__(
        self,
        log_t: str,
        person_index: Optional[int] = None,
        person_email: Optional[str] = None,
    ) -> None: ...
    @property
    def get_person_model(self) -> UsersPydantic: ...

    @property
    def get_email(self) -> str: ...

    @property
    def get_index(self) -> int: ...

    @staticmethod
    def _is_person(value=None) -> bool: ...

    @property
    def get_key_cache(self) -> str: ...

    def _is_key_of_cache(self, value: str) -> bool: ...


class PersonServiceDatabaseAdapter:
    """
    Here we have the two variables for works with the person database.
     - This service will allow us to get the one user by email or index, or create_or_update  one position from database.
        Make the check - we have a specific email/index of the person or not.
        For checking we have a two entry point. This is a 'user_id' and 'user_email'.
    """

    @staticmethod
    def get_user_by_id(user_id: Optional[int] = None) -> Optional[UsersPydantic]: ...

    @staticmethod
    def get_user_by_email(
        user_email: Optional[str] = None,
    ) -> Optional[UsersPydantic]: ...

    @staticmethod
    def search_by_email(user_email: str) -> list[Optional[UsersPydantic]]: ...

    @staticmethod
    def is_email(user_email: str) -> bool: ...

    @staticmethod
    def is_password(user_data: dict) -> bool: ...

    @staticmethod
    def create_or_update_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
    ) -> UsersPydantic: ...


class PostmanAdapter(Protocol):

    database_service: ClassVar[Optional[PersonServiceDatabaseAdapter]]
    lock: ClassVar[Optional[asyncio.Lock]]

    def __init__(self) -> None: ...

    class SubPerson(Protocol):
        def __init__(
            self,
            person_index: Optional[int],
            person_email: Optional[str],
        ) -> None: ...

        async def get_model(
            self, database_service: PersonServiceDatabaseAdapter, key_cache=""
        ) -> Optional[list[dict]]: ...

        def _get_data(
            self, email: str, database_service: PersonServiceDatabaseAdapter
        ) -> Optional[list[dict]]: ...

        @staticmethod
        def __get_cache(value: str) -> Optional[dict | list[bytes]]: ...

    @staticmethod
    def send_email_to_user(
        database_service: PersonServiceDatabaseAdapter,
        subject_: str,
        message_: str,
        user_id_: Optional[int],
        user_email_: Optional[str] = None,
    ) -> bool: ...
