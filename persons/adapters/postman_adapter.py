"""
persons/adapters/postman_adapter.py:1
"""

import asyncio
import json
import logging
from typing import Coroutine, Optional

from django.core.mail import send_mail
from django.db.models.expressions import result

from persons.interfaces import (
    PersonServiceDatabaseAdapter as PersonServiceDatabaseInitialize,
)
from persons.interfaces import (
    UsersDict,
    UsersPydantic,
)

from .. import EnumTemplatesREGEX
from ..exceptions import PersonErrorImproperlyConfigured
from ..exceptions.error_postman import PostmanRequiredModelError
from .person_base import PersonBasisMixin

#


log = logging.getLogger(__name__)


class PostmanAdapter:
    lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        """
        :param KEY_OF_CACHE_REGEX: This is the templates of regex for the check the value on the view line.
            Default belong the three expressions. Example this one from other: "r'(?P<name_all>user:pending:*)'".
            Response will be how "<re.Match object; span=(0, 14), match='user:pending:*'>" or 'None'.
        :param list | tuple args:
        :param dict kwargs:
        """
        from persons.adapters import PersonServiceDatabaseAdapter

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
            Sub_class for works wih properties of the one person. They are updating through entrypoint, cache and  database.
            === For get & update data.
            Here we have the two variables for works with the person database.
             - 'database_service' will allow us to get the one user by:
             - - an email address or
             - - index. It is database.
             And. We have the three variables for works with the cache data.
             - - ... or
             - - ...,
             - - value/cache_key, It is for cache.
             The method get_model for the:
             - get new data from source,
             - get simple - None. It if we hadn't found data.

             By email address or index we look up the person data in database and only database.
             When we have the 'value' (cache key) from collection 'EnumTemplatesKeysCache' (by path persons/__init__.py)
             mean we can look up data in the cache server and then update data in database.

             When user registrate, first his data go in database and same data is sending in cache server.
             After,  all moves persons (by a site), first is updating data in cache and then only will be to update data in database.

            :param int person_index: It is an index of person.
            :param str person_email: It is a email address.
            """
            from persons.services import CacheManager

            self.log_t = "[%s]:" % self.__class__.__name__
            super().__init__(self.log_t, person_index, person_email)
            log.info(
                f"\n[SubPerson][get_model]: DEBUG person_index: {self.get_index} & get_email: {self.get_email}"
            )
            self.cachemanager = CacheManager()
            self.value_of_cache: Optional[list[bytes] | dict] = []

        async def get_model(
            self, database_service: PersonServiceDatabaseInitialize, key_cache: str = ""
        ) -> Optional[dict]:
            """
            Entrypoint is only 'self.get_index' & 'self.get_email',
            # First - Check (lock up) in cache server. Here we will look the similar state.
            # If we could do not find the similar data then we will be looking to the relation database.
            Note: This method hase only one the cache key- 'user:pending:login'.
            :param database_service:PersonServiceDatabaseInitialize. Required
            :param cachemanager: CacheManagerInitialiae. Required
            :param key_cache: str = ""
            :return:
            """

            try:
                get_index = self.get_index
                get_email = self.get_email
                user_old = None
                get_person_model = self.get_person_model
                user_old: Optional[UsersPydantic] = None
                if get_person_model is None and get_email is None and get_index is None:
                    raise PersonErrorImproperlyConfigured()
                # ====== Take the old model of user/person. Find data in the cache
                # per template "user:pending:login". If we got the data, it means next we will be
                # updating the model (contain the old tada).
                # Object
                if get_person_model is not None and isinstance(
                    get_person_model, UsersPydantic
                ):
                    pass

                # Index
                elif get_index is not None:
                    # ====== Take the user's index, lookup the old user's model. Then is finding the user's data in
                    # the cache how above.
                    async with PostmanAdapter.lock:

                        def get_user_by_index_sync(index):
                            return database_service.get_user_by_id(index)

                        user_old = await asyncio.to_thread(
                            get_user_by_index_sync, get_index
                        )

                # Email
                elif get_email is not None and isinstance(get_email, str):
                    # ====== Take the user's email, lookup the old user's model. Then is finding the user's data in
                    async with PostmanAdapter.lock:

                        def get_user_by_email_sync(email):
                            return database_service.get_user_by_email(email)

                        user_old = await asyncio.to_thread(
                            get_user_by_email_sync, get_email
                        )

                if user_old is None:
                    return None
                self.get_person_model = user_old
                del user_old

                get_data = await self._get_data(
                    key_cache,
                    database_service,
                )
                return get_data
            except Exception as e:
                log.warning(" ".join([self.log_t, e.args[0] if e.args else str(e)]))
                return None

        async def _get_data(
            self,
            value: str,
            database_service: PersonServiceDatabaseInitialize,
        ) -> Optional[dict]:
            """
            Value - it is a key of cache. Through the cache server we are receiving data (or None).

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
            #     When we are having the key 'user:pending:login' mean for lookup the person's data needed < EMAIL >.
            #         [item for item < VALUE OF user:pending:login> if item['email'] == email]
            # Note: You can send the total template  through value. It is the 'user:pending:%s' or 'user:pending:letter:%s'.
            #     It will return the total list from the keys: '["user:pending:< USER EMAIL one >",
            #                                                  "user:pending:< USER EMAIL next >",
            #                                                  "user:pending:< USER EMAIL more if be having >"]'.

            :return: dist or None. Dictionary  data for publication.
            """
            # ============================================
            # CACHE
            # ============================================
            # Check a key on the valid.
            data_of_cache_list: list = []

            log.info("[SubPerson][_get_data]: DEBUG BEFORE GET COROUTINE")
            await self.cachemanager.aget(
                key=value, collection=self.value_of_cache, exat=86400
            )
            log.info(
                f"[SubPerson][_get_data]: DEBUG BEFORE received the data_from_cache_server Type: {type(self.value_of_cache)}"
            )
            log.info(
                f"[SubPerson][_get_data]: DEBUG BEFORE received the data_from_cache_server: {str(self.value_of_cache)}"
            )
            data_from_cache_server: Optional[bytes | list | dict] = (
                self.value_of_cache.copy()
            )
            self.value_of_cache.clear()
            # Value
            # List of bytes
            log.info(" DEBUG [SubPerson][_get_data]:  1")
            if (
                isinstance(data_from_cache_server, list)
                and len(data_from_cache_server) > 0
            ):
                log.info(" DEBUG [SubPerson][_get_data]:  2")
                for data_from_cache_server_bytes in data_from_cache_server:
                    log.info(" DEBUG [SubPerson][_get_data]:  3")
                    data_from_cache_json = json.loads(
                        data_from_cache_server_bytes.decode()
                    )
                    if isinstance(data_from_cache_json, dict):
                        log.info(" DEBUG [SubPerson][_get_data]:  4")
                        data_of_cache_list.append(data_from_cache_json)
                    else:
                        [
                            data_of_cache_list.append(item)
                            for item in data_from_cache_json
                        ]
                        log.info(
                            f" DEBUG [SubPerson][_get_data]:  5 data_of_cache_list: {str(data_of_cache_list)} & data_from_cache_json: {str(data_from_cache_json)}"
                        )

            # Dict
            elif isinstance(data_from_cache_server, dict):
                log.info(" DEBUG [SubPerson][_get_data]:  6")
                data_of_cache_list.append(data_from_cache_server)

            else:

                raise PostmanRequiredModelError(
                    self.log_t[:-1]
                    + f"[{self._get_data.__name__}]: "
                    + "Data is not valid."
                )
            # Updating data
            for item_dict in data_of_cache_list.copy():
                # if not isinstance(item_dict, bytes):
                log.info(
                    f" DEBUG [SubPerson][_get_data]:  9 item_dict: {str(item_dict)}"
                )

                try:

                    persons_index = self.get_index
                    persons_email = self.get_email
                    log.info(
                        f"""\n
                    # ============================================
                    # DEBUG [SubPerson][_get_data]: 12 \n
                    # after persons_index:  {persons_index}
                    # after person_email: {persons_email}
                    # after item_dict:  {item_dict}
                    # ============================================
"""
                    )

                    # UPDATE - A)
                    def create_or_update_in_database_sync():
                        return database_service.create_or_update_in_database(
                            user_data=item_dict,
                            user_id=persons_index,
                            user_email=persons_email,
                        )

                    update_user_valid: Optional[dict] = await asyncio.to_thread(
                        create_or_update_in_database_sync
                    )
                    return update_user_valid
                except Exception as e:
                    raise ValueError(
                        self.log_t[:-1] + f"[{self._get_data.__name__}]: " + str(e)
                    )
            return None

    @staticmethod
    def send_email_to_user(
        database_service: PersonServiceDatabaseInitialize,
        subject_: str,
        message_: str,
        user_id_: Optional[int],
        user_email_: Optional[str] = None,
    ) -> bool:
        """Returning the True or mistake"""

        """Send email (in the database Person)"""
        if user_id_ is None and user_email_ is None:
            raise PersonErrorImproperlyConfigured()
        try:
            user_old = (
                database_service.get_user_by_email(user_email=user_email_)
                if user_id_ is not None
                else database_service.get_user_by_id(user_id=user_id_)
            )
            if user_old is not None:
                send_mail(
                    subject=subject_,
                    message=message_,
                    recipient_list=[user_old.email],
                    from_email="host_test@email.ru",
                )
                return True
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        return False
