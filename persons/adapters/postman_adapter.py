"""
persons/adapters/postman_adpter.py:1
"""

import asyncio
import json
import logging
from typing import Optional

from django.core.mail import send_mail

from persons.interfaces import PersonServiceInitialize, UsersPydantic

from .. import EnumTemplatesKeysCache, EnumTemplatesREGEX
from ..exceptions import PersonErrorImproperlyConfigured
from ..interfaces import EmailString
from . import CacherAdapterMixin
from .person_base import PersonBasisMixin

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
            person_email: Optional[str] = None,
        ) -> None:
            self.log_t = "[%s]:" % self.__class__.__name__
            super().__init__(self.log_t, person_index, person_email)
            log.info(
                f"\n[SubPerson][get_model]: TEST DEBUG person_index: {self.get_index} & get_email: {self.get_email}"
            )

        async def get_model(
            self, lock: asyncio.Lock, database_service: PersonServiceInitialize
        ) -> Optional[dict] | None:
            """
            # First - Check (lock up) in cache server. Here we will look the similar state.
            # If we could do not find the similar data then we will be looking to the relation database.
            :return:
            """

            try:
                get_index = self.get_index
                get_email = self.get_email
                user_old = None
                log.info(
                    f"[SubPerson][get_model]: TEST DEBUG get_email: {get_email} & get_index {get_index}"
                )
                get_person_model = self.get_person_model
                if get_person_model is None and get_email is None and get_index is None:
                    raise PersonErrorImproperlyConfigured()
                log.info("TEST DEBUG 0")
                # ====== Take the old model of user/person. Find data in the cache
                # per template "user:pending:login:%s". If we got the data means, next we will be
                # updating the model (contain the old tada).
                if get_person_model is not None and isinstance(
                    get_person_model, UsersPydantic
                ):
                    log.info("TEST DEBUG 1")
                    log.info(
                        "[SubPerson][get_model]: # ====== Take the old model of user/person. Find data in the cache"
                    )
                    email_fra: str = get_person_model.__getattribute__("email")
                    return self._get_data(email_fra, database_service)
                elif get_index is not None and isinstance(get_index, int):
                    # ====== Take the user's index, lookup the old user's model. Then is finding the user's data in
                    # the cache how above.
                    log.info("TEST DEBUG 2")
                    log.info(
                        "[SubPerson][get_model]: TEST DEBUG # ====== Take the user's index, lookup the old user's model. Then is finding the user's data in"
                    )

                    async with lock:
                        user_old = database_service.get_user_by_id(get_index)

                    if user_old is None:
                        return None
                    # self.get_person_model = user_old
                    log.info(
                        f"TEST DEBUG FROM 2: TYPE: {type(user_old)} % EMAIL {str(user_old)} "
                    )
                    email_fra: str = user_old.__getattribute__("email")
                    log.info("TEST DEBUG FROM 2: EMAIL " + email_fra)
                    return self._get_data(email_fra, database_service)
                elif get_email is not None and isinstance(get_email, str):
                    log.info("TEST DEBUG 3")
                    # ====== Take the user's email, lookup the old user's model. Then is finding the user's data in
                    # the cache how above.
                    async with lock:
                        user_old = database_service.get_user_by_email(get_email)
                    if user_old is not None:
                        self.get_person_model = user_old
                    log.info("TEST DEBUG FROM 3: EMAIL " + get_email)

                    return self._get_data(get_email, database_service)

                return None
            except Exception as e:
                log.warning(" ".join([self.log_t, e.args[0] if e.args else str(e)]))
                return None

        def _get_data(
            self, email: str, database_service: PersonServiceInitialize
        ) -> Optional[dict]:
            """
            On the entrypoint we are receiving the user's 'email'. THe email is a sub-text (prefix) for key of cache.
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

            data_from_cache_server_list: list | None = self.__get_cache(key_cache)
            log.info(
                f"[SubPerson][_get_data]: TEST DEBUG BEFORE received the data_from_cache_server_list Type: {type(data_from_cache_server_list)}"
            )
            log.info(
                f"[SubPerson][_get_data]: TEST DEBUG BEFORE received the data_from_cache_server_list: {str(data_from_cache_server_list)}"
            )
            for data_from_cache_server_bytes in data_from_cache_server_list:
                data_from_cache_server = json.loads(
                    data_from_cache_server_bytes.decode()
                )
                result_bool = isinstance(data_from_cache_server, dict)

                if result_bool:
                    try:
                        log.info("TEST DEBUG before user_from_database")

                        user_from_database = database_service.get_user_by_email(
                            data_from_cache_server["email"]
                        )
                        log.info("TEST DEBUG after user_from_database")
                        user_from_database_json = user_from_database.model_dump_json()
                        log.info(
                            f"[SubPerson][_get_data]: TEST DEBUG after user_from_database: TYPE: {type(json.loads(user_from_database_json))} & {str(user_from_database_json)}"
                        )
                        ud = json.loads(user_from_database_json)
                        [
                            setattr(ud, k, v)
                            for k, v in data_from_cache_server.items()
                            if hasattr(ud, k)
                        ]
                        log.info("TEST DEBUG after setattr(ud)")
                        database_service.create_or_update_in_database(user_data=ud)
                        log.info(
                            "TEST DEBUG after database_service.create_or_update_in_database"
                        )
                        return ud
                    except Exception as e:
                        raise ValueError(
                            self.log_t[:-1] + f"[{self._get_data.__name__}]: " + str(e)
                        )
            return None

        @staticmethod
        def __get_cache(value: str) -> dict | list | None:
            from persons.apps import cachemanager

            log.info(f"[SubPerson][__get_cache]: DEBUG {value}")
            # value_of_cache: Optional[bytes] = None
            value_of_cache: Optional[list | dict] = []
            # ============================================
            # CONNECT TO THE CACHE SERVER
            # ============================================
            try:
                cachemanager.get(key=value, collection=value_of_cache, exat=86400)
                return value_of_cache
            except Exception as e:
                log.error(
                    f"[SubPerson][__get_cache]: {e.args[0] if e.args else str(e)}"
                )
                raise e
            # related_bool = PostmanAdapter.related()
            # if related_bool:
            #     with PostmanAdapter.connected() as conn:
            #
            #         try:
            #             value_of_cache: bytes | None = conn.getex(value, exat=86400)
            #         except Exception as e:
            #             raise e
            #     if value_of_cache is None:
            #         return None
            #     return json.loads(value_of_cache.encode("utf-8"))
            # return None

    @staticmethod
    def send_email_to_user(
        lock: asyncio.Lock,
        database_service: PersonServiceInitialize,
        subject_: str,
        message_: str,
        user_id_: Optional[int],
        user_email_: Optional[str] = None,
    ) -> bool:
        """Returning the True or mistake"""
        # from persons.models import Users

        """Send email (in the database Person)"""
        if user_id_ is None and user_email_ is None:
            raise PersonErrorImproperlyConfigured()
        try:
            log.info(
                f"""\n
                # PostmanAdapter.send_email_to_user
                # ============================================
                # SEND EMAIL BY the user id or user email
                # ============================================
                # user_id_: {str(user_id_)}
                # user_email_: {str(user_email_)}
                # subject_: {str(subject_)}
                # message_: {str(message_)}
                """
            )

            user_old = (
                database_service.get_user_by_email(user_email=user_email_)
                if user_id_ is not None
                else database_service.get_user_by_id(user_id=user_id_)
            )
            if user_old is not None:
                log.info(
                    f"""\n
                    # ============================================
                    # SEND EMAIL AFTER  SEARCH BY user_id_ or user_email_
                    # ============================================
                    # user: {str(user_old)}
                    """
                )
                send_mail(
                    subject=subject_,
                    message=message_,
                    recipient_list=[user_old.email],
                    from_email="host_test@email.ru",
                )
                # user.email_user(
                #     subject=subject_,
                #     message=message_,
                #     from_email="host_test@email.ru",
                # )
                return True
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        return False
