"""
persons/adapters/postman_adapter.py:1
"""

import asyncio
import json
import logging
import re
from typing import Optional

from django.core.mail import send_mail

from persons.interfaces import (
    PersonService,
)
from persons.interfaces import (
    PersonServiceDatabaseAdapter as PersonServiceDatabaseInitialize,
)
from persons.interfaces import (
    UsersDict,
    UsersPydantic,
)

from .. import EnumTemplatesKeysCache, EnumTemplatesREGEX
from ..exceptions import PersonErrorImproperlyConfigured
from ..exceptions.error_postman import PostmanRequiredModelError
from ..interfaces import EmailString
from . import CacherAdapterMixin, PersonServiceDatabaseAdapter
from .person_base import PersonBasisMixin

#


log = logging.getLogger(__name__)


class PostmanAdapter(
    CacherAdapterMixin,
):
    database_service = None
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
        The Postman. It is a builder. It contains the:
            - interface of cache-server through the 'persons.apps.cachemanager';
            - account service/manager. It is for a work through email. It is sending a secret token or the integer code
              fnd more it is for account actions. 'persons.apps.accountmanager';
            - emailing. It is a simply sending a message/email to the user's email address
                through 'PostmanAdapter.send_email_to_user';
            - service of database. It is a work with a searching, getting of user by email or id, checking of
                email address, password in relation database (It not Redis) - 'database_service = PersonServiceDatabaseAdapter'.

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
        from .person_database_adapter import PersonServiceDatabaseAdapter

        cls.KEY_OF_CACHE_REGEX = EnumTemplatesREGEX.PERSON_KEYS_OF_CACHE_IN_REGEX.value
        cls.log_t: str = "[%s]" % cls.__class__.__name__
        initialization = super().__new__(cls, *args, **kwargs)
        initialization.database_service = PersonServiceDatabaseAdapter()

        return initialization

    class SubPerson(PersonBasisMixin):

        def __init__(
            self,
            person_index: Optional[int] = None,
            person_email: Optional[str] = None,
        ) -> None:
            """
            Important! This person must be having a status is_authenticated or not is_nonymous!
            Sub_class for works wih properties and cache or database of Person.
            Here we have the two variables for works with the person database.
             - 'database_service' will allow us to get the one user by email or index, or create_or_update  one position from database.
                Make the check - we have a specific email/index of the person or not.
            :param int person_index: It is an index of person.
            :param str person_email: It is a email address.
            """
            self.log_t = "[%s]:" % self.__class__.__name__
            super().__init__(self.log_t, person_index, person_email)
            log.info(
                f"\n[SubPerson][get_model]: TEST DEBUG person_index: {self.get_index} & get_email: {self.get_email}"
            )

        async def get_model(
            self, database_service: PersonServiceDatabaseInitialize
        ) -> Optional[list[dict]]:
            """
            Entrypoint is only 'self.get_index' & 'self.get_email',
            # First - Check (lock up) in cache server. Here we will look the similar state.
            # If we could do not find the similar data then we will be looking to the relation database.
            Note: This method hase only one the cache key- 'user:pending:login'.
            :return:
            """

            try:
                get_index = self.get_index
                get_email = self.get_email
                user_old = None
                key_cache: str = ""
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
                # Object
                if get_person_model is not None and isinstance(
                    get_person_model, UsersPydantic
                ):
                    log.info("TEST DEBUG 1")
                    log.info(
                        "[SubPerson][get_model]: # ====== Take the old model of user/person. Find data in the cache"
                    )
                    email_fra: str = get_person_model.__getattribute__("email")

                # Index
                elif get_index is not None and isinstance(get_index, int):
                    # ====== Take the user's index, lookup the old user's model. Then is finding the user's data in
                    # the cache how above.
                    log.info("TEST DEBUG 2")
                    log.info(
                        "[SubPerson][get_model]: TEST DEBUG # ====== Take the user's index, lookup the old user's model. Then is finding the user's data in"
                    )

                    async with PostmanAdapter.lock:
                        user_old = database_service.get_user_by_id(get_index)

                    if user_old is None:
                        return None
                    # self.get_person_model = user_old
                    log.info(
                        f"TEST DEBUG FROM 2: TYPE: {type(user_old)} % EMAIL {str(user_old)} "
                    )
                    email_fra: str = user_old.__getattribute__("email")
                    log.info("TEST DEBUG FROM 2: EMAIL " + email_fra)
                    get_email = email_fra

                    log.info("TEST DEBUG FROM 2: KEY CACHE " + key_cache)
                # Email
                elif get_email is not None and isinstance(get_email, str):
                    log.info("TEST DEBUG 3")
                    # ====== Take the user's email, lookup the old user's model. Then is finding the user's data in
                    async with PostmanAdapter.lock:
                        log.info("TEST DEBUG BEFORE 3: EMAIL " + get_email)

                        user_old = database_service.get_user_by_email(get_email)

                        log.info(
                            "TEST DEBUG AFTER 3: "
                            + str(type(user_old) == UsersPydantic)
                        )
                        log.info(
                            "TEST DEBUG AFTER TYPE 3: EMAIL " + str(type(user_old))
                        )
                        log.info("TEST DEBUG AFTER 3: EMAIL " + str(user_old.email))
                    if user_old is not None:
                        self.get_person_model = user_old
                    log.info("TEST DEBUG FROM 3: EMAIL " + get_email)

                    log.info("TEST DEBUG FROM 3: key_cache: " + key_cache)
                key_cache += EnumTemplatesKeysCache.USER_PENDING_LOGIN.value
                return self._get_data(key_cache, database_service, get_email)
            except Exception as e:
                log.warning(" ".join([self.log_t, e.args[0] if e.args else str(e)]))
                return None

        def _get_data(
            self,
            value: str,
            database_service: PersonServiceDatabaseInitialize,
            email=None,
        ) -> Optional[list[dict]]:
            """
            Value - it is a key of cache. From cache ser we are receiving the data or None.

            :param value: Required. It is a key! *lok to the 'persons.EnumTemplatesKeysCache'*.
                It is the key in the cache server. It is simply template key.
                Example: key 'user:pending:login' or
                 key 'user:pending:letter:< EMAIL >' & more.
                 Note: If we have key the:
                  - 'user:pending:letter:< EMAIL >' & some the templates keys '...:...:< EMAIL >' it mean value will be
                    the string  '{"username": < USERNAME >, "email": < EMAIL >, ...}'
                  - 'user:pending:login' it mean value will be the string b'"[{'is_superuser': < bool >,
                    'email': < EMAIL >,'category': < user_CATEGORY >},]"'.
            :param database_service: Required. This is an object from the 'PersonServiceDatabaseAdapter()'.
            # :param email: This is the email of a person.
            #     The cache's key 'user:pending:login' have the list how the bytes line.
            #     When we have the key 'user:pending:login' mean for lookup the person's data needed < EMAIL >.
            #         [item for item < VALUE OF user:pending:login> if item['email'] == email]
            # Note: You can send the total template  through value. It is the 'user:pending:%s' or 'user:pending:letter:%s'.
            #     It will return the total list from the keys: '["user:pending:< USER EMAIL one >",
            #                                                  "user:pending:< USER EMAIL next >",
            #                                                  "user:pending:< USER EMAIL more if be having >"]'.

            :return: dist or None
            """

            # Value & Email

            # Check a key on the valid.
            PostmanAdapter.get_key_cache = value
            key_cache = PostmanAdapter.get_key_cache
            data_list: list = []
            data_from_cache_server: Optional[bytes | list | dict] = self.__get_cache(
                key_cache
            )
            log.info(
                f"[SubPerson][_get_data]: TEST DEBUG BEFORE received the data_from_cache_server_list Type: {type(data_from_cache_server)}"
            )
            log.info(
                f"[SubPerson][_get_data]: TEST DEBUG BEFORE received the data_from_cache_server_list: {str(data_from_cache_server)}"
            )
            # None
            if key_cache is not None:
                return None

            # Value
            # List
            if isinstance(data_from_cache_server, list):
                for data_from_cache_server_bytes in data_from_cache_server:
                    data_list.append(json.loads(data_from_cache_server_bytes.decode()))

            # Dict
            elif isinstance(data_from_cache_server, dict):
                data_list.append(data_from_cache_server)

            elif isinstance(data_from_cache_server, list):
                data_list.extend(data_from_cache_server)

            else:
                raise PostmanRequiredModelError(
                    self.log_t[:-1]
                    + f"[{self._get_data.__name__}]: "
                    + "Data is not valid."
                )

            # Updating data
            for item_dict in data_list:
                if not isinstance(item_dict, bytes):
                    # Need get one person.
                    data_list_new: list[UsersDict] = [
                        item for item in item_dict if item["email"] == email
                    ]
                    data_list.clear()
                    if len(data_list_new) > 0:
                        item_dict = data_list_new[0]
                    else:
                        return None
                    del data_list_new
                try:
                    log.info("TEST DEBUG before user_from_database")
                    # Database
                    user_from_database = database_service.get_user_by_email(
                        item_dict["email"]
                    )
                    log.info("TEST DEBUG after user_from_database")
                    user_from_database_json = user_from_database.model_dump_json()
                    log.info(
                        f"[SubPerson][_get_data]: TEST DEBUG after user_from_database: TYPE: {type(json.loads(user_from_database_json))} & {str(user_from_database_json)}"
                    )
                    ud = json.loads(user_from_database_json)
                    [setattr(ud, k, v) for k, v in item_dict.items() if hasattr(ud, k)]
                    log.info("TEST DEBUG after setattr(ud)")
                    database_service.create_or_update_in_database(user_data=ud)
                    log.info("Data of the cache's server was updated with new values.")

                    data_list.append(ud)
                except Exception as e:
                    raise ValueError(
                        self.log_t[:-1] + f"[{self._get_data.__name__}]: " + str(e)
                    )

            return data_list

        @staticmethod
        def __get_cache(value: str) -> dict | list[bytes] | None:
            from persons.apps import cachemanager

            log.info(f"[SubPerson][__get_cache]: DEBUG {value}")
            # value_of_cache: Optional[bytes] = None
            value_of_cache: Optional[list[bytes] | dict] = []
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
        database_service: PersonServiceDatabaseInitialize,
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
