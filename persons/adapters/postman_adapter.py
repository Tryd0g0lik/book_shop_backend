"""
persons/adapters/postman_adpter.py:1
"""

import asyncio
import json
import logging
from typing import Optional

from pydantic import EmailStr

from persons.interfaces import UsersPydantic

from .. import EnumTemplatesKeysCache, EnumTemplatesREGEX
from ..exceptions import PersonErrorImproperlyConfigured
from ..interfaces import EmailString
from . import CacherAdapterMixin

# from .cache_base import CacherBaseMixin
from .person_base import PersonBasisMixin
from .person_service_adapter import PersonServiceAdapter

# from django.db.models.expressions import result
# from watchfiles import awatch


log = logging.getLogger(__name__)


class PostmanAdapter(
    CacherAdapterMixin,
):
    lock = asyncio.Lock()

    def __init__(
        self,
        db: int = 0,
        max_connections: int = 5,
        decode_responses: bool = False,
        socket_connect_timeout: int = 5,
        socket_timeout: int = 5,
        retry_on_timeout: bool = True,
        health_check_interval: int = 30,
    ):
        """
        This is the Postman. The work with a cache-server and the SubPerson
        :param db:
        :param max_connections:
        :param decode_responses:
        :param socket_connect_timeout:
        :param socket_timeout:
        :param retry_on_timeout:
        :param health_check_interval:
        """
        super().__init__(
            db,
            max_connections,
            decode_responses,
            socket_connect_timeout,
            socket_timeout,
            retry_on_timeout,
            health_check_interval,
        )

    def __new__(cls, *args, **kwargs):
        """
        :param KEY_OF_CACHE_REGEX: This is the templates of regex for the check the value on the view line.
            Default belong the three expressions. Example this one from other: "r'(?P<name_all>user:pending:*)'".
            Response will be how "<re.Match object; span=(0, 14), match='user:pending:*'>" or 'None'.
        :param list | tuple args:
        :param dict kwargs:
        """
        cls.log_t: str = "[%s]" % cls.__class__.__name__
        cls.KEY_OF_CACHE_REGEX = EnumTemplatesREGEX.PERSON_KEYS_OF_CACHE_IN_REGEX.value

        return super().__new__(cls)

    class SubPerson(PersonBasisMixin):
        def __init__(
            self,
            person_index: Optional[int] = None,
            person_email: Optional[EmailStr] = None,
        ) -> None:
            self.log_t = "[%s]:" % self.__class__.__name__
            super().__init__(self.log_t, person_index, person_email)

            self.database_service = PersonServiceAdapter()

        async def get_model(self, lock: asyncio.Lock) -> UsersPydantic | None:
            """
            # First - Check the cache server. Here we will look the similar state.
            # If we could be not find the similar data then we will be looking to the relation database.
            :return:
            """

            try:
                async with lock:
                    get_index = self.get_index
                    get_email = self.get_email
                    get_person_model = self.get_person_model
                    if (
                        get_person_model is None
                        and get_email is not None
                        and get_index is not None
                    ):
                        raise PersonErrorImproperlyConfigured()
                    # ====== Take the old model of user/person. Find data in the cache
                    # per template "user:pending:login:%s". If we got the data means, next we will be
                    # updating the model (contain the old tada).
                    if get_person_model is not None and isinstance(
                        get_person_model, UsersPydantic
                    ):
                        email_fra: EmailString = get_person_model.__getattr__("email")
                        return self._get_data(email_fra)
                    elif get_index is not None and isinstance(get_index, int):
                        # ====== Take the user's index, lookup the old user's model. Then is finding the user's data in
                        # the cache how above.
                        user_old = self.database_service.get_user_by_id(get_index)
                        if user_old is None:
                            return None
                        self.get_person_model = user_old
                        email_fra: EmailString = user_old.__getattr__("email")
                        return self._get_data(email_fra)
                    elif get_email is not None and isinstance(get_email, EmailString):
                        # ====== Take the user's email, lookup the old user's model. Then is finding the user's data in
                        # the cache how above.
                        user_old = self.database_service.get_user_by_email(get_email)
                        if user_old is None:
                            return None
                        self.get_person_model = user_old
                        return self._get_data(get_email)

                    return None
            except Exception as e:
                from django.apps import apps
                from wagtail.compat import AUTH_USER_MODEL

                log.warning(" ".join([self.log_t, e.args[0] if e.args else str(e)]))
                # persons = apps.get_model(AUTH_USER_MODEL)

        def _get_data(self, email) -> Optional[dict]:
            """
            On the entrypoint we are receiving the user's 'email'. This email it is a sub-text (prefix) for a key of cache.
            After we received the cache's key (it is template "user:pending:login:%s") next we request to the redis cache server.
            If key (with contain the email) now exists on the cache-server mean we are receiving data that stores
                a fresh state or None.
            If this is the data stores the refresh state mean - updating the database and return the dict of data.
            :param EmailString email: Email address of user.
            :return: dist or None
            """
            key_cache: str = EnumTemplatesKeysCache.USER_PENDING_LOGIN_0.value % str(
                email
            )
            PostmanAdapter.get_key_cache = key_cache

            data_from_cache_server: dict | None = self.__get_cache(key_cache)
            if isinstance(data_from_cache_server, dict):
                UsersPydantic.model_validate(**data_from_cache_server)
                self.database_service.update_user_in_database(
                    data_from_cache_server,
                )
                self.get_person_model = {**data_from_cache_server}
                return self.get_person_model
            return None

        @staticmethod
        def __get_cache(value: str) -> dict | list | None:

            value_of_cache: Optional[bytes] = None
            # ============================================
            # CONNECT TO THE CACHE SERVER
            # ============================================
            related_bool = PostmanAdapter.related()
            if related_bool:
                with PostmanAdapter.connected() as conn:

                    try:
                        value_of_cache: bytes | None = conn.getex(value, exat=86400)
                    except Exception as e:
                        raise e
                if value_of_cache is None:
                    return None
                return json.loads(value_of_cache.encode("utf-8"))
            return None
