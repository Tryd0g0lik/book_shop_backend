"""
persons/adapters/person_service_adapter.py:6

This is service for a work only with a business logic for the Users (Persons)
"""

import json
import logging
from threading import Thread
from typing import Optional

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.exceptions import SynchronousOnlyOperation
from django.utils.hashable import make_hashable

from persons.exceptions import PersonErrorImproperlyConfigured
from persons.interfaces import UsersPydantic
from persons.interfaces.interface_persons import UsersPydanticDict
from project.settings import SECRET_KEY

log = logging.getLogger(__name__)


class PersonServiceDatabaseAdapter:
    """
    Here we have the two variables for works with the person database.
     - This service will allow us to get the one user by email or index, or create_or_update  one position from database.
        Make the check - we have a specific email/index of the person or not.
        For checking we have a two entry point. This is a 'user_id' and 'user_email'.
    """

    @staticmethod
    def get_user_by_id(user_id: Optional[int] = None) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        from persons.models import Users

        try:
            if user_id is not None and isinstance(user_id, int):
                user = Users.objects.get(id=user_id)
                return UsersPydantic.model_validate(user)
        except Users.DoesNotExist:
            return None
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def get_user_by_email(
        user_email: Optional[str] = None,
    ) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        from persons.models import Users
        from persons.services import CustomizationSyncAsyncLoop

        try:
            if user_email is not None and isinstance(user_email, str):
                user_list = []
                try:
                    u = Users.objects.get(email=user_email)
                    user_list.append(u)
                except SynchronousOnlyOperation:

                    def get_result():
                        u = Users.objects.get(email=user_email)
                        user_list.append(u)

                    custom_loop = CustomizationSyncAsyncLoop()
                    custom_loop.get_new_function = get_result
                    wrapper = custom_loop.get_new_loop()
                    thread = Thread(target=wrapper)
                    thread.start()
                    thread.join(timeout=8)
                    logging.debug(f"Thread status after join(): {thread.is_alive()}")
                return (
                    UsersPydantic.model_validate(user_list[0])
                    if len(user_list) > 0
                    else None
                )
        except Users.DoesNotExist:
            return None
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        return None

    @staticmethod
    def search_by_email(user_email: str) -> list[UsersPydantic]:
        """Search users by email"""
        from persons.models import Users
        from persons.services import CustomizationSyncAsyncLoop

        users = []
        try:
            u = Users.objects.filter(email__icontains=user_email)
            users.extend(u)
        except SynchronousOnlyOperation:

            def get_result():
                u = Users.objects.filter(email__icontains=user_email)
                users.extend(u)

            custom_loop = CustomizationSyncAsyncLoop()
            custom_loop.get_new_function = get_result
            wrapper = custom_loop.get_new_loop()
            thread = Thread(target=wrapper)
            thread.start()
            thread.join(timeout=8)
            logging.debug(f"Thread status after join(): {thread.is_alive()}")
            return (
                [UsersPydantic.model_validate(u) for u in users]
                if len(users) > 0
                else []
            )
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def save(user_dict: dict) -> list[UsersPydantic]:
        """Save data users by email"""
        from persons.models import Users
        from persons.services import CustomizationSyncAsyncLoop

        user_list = []
        try:
            user = Users.objects.create(**user_dict)
            user_list.append(user)

        except SynchronousOnlyOperation:

            def get_result():
                u = Users.objects.create(**user_dict)
                user_list.append(u)

            custom_loop = CustomizationSyncAsyncLoop()
            custom_loop.get_new_function = get_result
            wrapper = custom_loop.get_new_loop()
            thread = Thread(target=wrapper)
            thread.start()
            thread.join(timeout=8)
            logging.debug(f"Thread status after join(): {thread.is_alive()}")

            return (
                [UsersPydantic.model_validate(user_list[0])]
                if len(user_list) > 0
                else []
            )
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def is_email(user_email: str) -> bool:
        """Search users by email"""
        from persons.models import Users
        from persons.services import CustomizationSyncAsyncLoop

        try:
            print(f"\n ------------------ \n DEBUG BEFORE. email:  {str(user_email)}")
            test_result = []
            try:
                u = Users.objects.get(email=user_email)
                test_result.append(u)
            except SynchronousOnlyOperation:

                def get_result():
                    u = Users.objects.get(email=user_email)
                    test_result.append(u)

                custom_loop = CustomizationSyncAsyncLoop()
                custom_loop.get_new_function = get_result
                wrapper = custom_loop.get_new_loop()
                thread = Thread(target=wrapper)
                thread.start()
                thread.join(timeout=8)
                logging.debug(f"Thread status after join(): {thread.is_alive()}")
            print(
                f"\n ------------------ \n\tDEBUG AFTER Users.objects cycle. email:  {str(test_result)}"
            )
            return True if len(test_result) > 0 else False
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def is_password(user_data: dict) -> bool:
        """
        TODO: изменить логику. Внести проверку хешированного пароля получая нужные данные из самой базе данных.
            На выход подать bool
        Search users by email
        """
        try:
            bool_list = [
                True if k in ["password", "password2", "password"] else False
                for k, _ in user_data.items()
            ]

            return bool_list[0]
        except Exception as e:
            raise e

    @staticmethod
    def create_or_update_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
    ) -> UsersPydantic:
        """
        TODO: user_data - обязательный атрибут.
            Если user_id или user_email не равно None. Значит данные на обновление,
            Если user_id и user_email отсутствуют. Значит создаём нового пользователя.,
            Если user_id или user_email не равно None:
             - Создаю нового подльзователя смотрим в кеше по ключу: user:pending:login:<EMAIL> - Проверить работу с кешем .
             Главно В этом файле работаю только с базой данных
             &
             Тут нет проверки паролей. Сравнение паролей - нового и старого хешированного должно проходить вне этого метода
             &
             Сюда пароль поступает в родительском состоянии . Тут хешируется перед сохранением.

        Args:
            :param user_data: Dictionary with fields to update
            :param user_id: User ID (optional)
            :param user_email: User email (optional)

        Returns:
            Updated user as Pydantic model
        """
        from persons.models import Users
        from persons.services import CustomizationSyncAsyncLoop

        get_person_model_old: Optional[UsersPydantic] = None
        em: Optional[str] = user_data.__getitem__("email")

        if user_id is not None:
            # ============================================
            # UPDATE USER FROM  DATABASE BY user_id
            # ============================================
            try:
                get_person_model_old = PersonServiceDatabaseAdapter.get_user_by_id(
                    user_id
                )
            except PersonErrorImproperlyConfigured as e:
                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        elif user_email is not None:
            # ============================================
            # UPDATE USER FROM  DATABASE BY user_email
            # ============================================
            try:
                get_person_model_old = PersonServiceDatabaseAdapter.get_user_by_email(
                    user_email
                )
            except PersonErrorImproperlyConfigured as e:
                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        if get_person_model_old is None and em is not None:
            # ============================================
            # CREATE NEW USER IN DATABASE
            # ============================================

            try:
                #                 is_user: bool = PersonServiceDatabaseAdapter.is_email(em)
                #                 log.info(f"TEST DEBUG AFTER is_user: {str(is_user)}")
                #
                #                 if is_user:
                #                     """
                #                     This mean - user already exists.
                #                     Return error message
                #                     """
                #                     raise PersonErrorImproperlyConfigured(
                #                         "User already exists was founded before it. \
                # Change the email address."
                #                     )
                keys_ = list(user_data.keys())
                keys_ = [
                    k for k in keys_ if k in ["password1", "password2", "password"]
                ]
                if len(keys_) == 0:
                    raise PersonErrorImproperlyConfigured(
                        "User's password not be found. "
                    )
                password_str = user_data.__getitem__(keys_[0])

                try:
                    # ============================================
                    # HASHING A USER'S PASSWORD
                    # ============================================
                    make_hashe = PBKDF2PasswordHasher()
                    password_hashed = make_hashe.encode(
                        password=password_str, salt=SECRET_KEY[:25]
                    )
                    log.info(
                        f"""\n\t
                    # ============================================
                    # TEST DEBUG create_or_update_in_database
                    # That is user_data: {str(user_data)}
                    # That is the type of user_data: {type(user_data)}
                    # password_hashed: {password_hashed}
                    # ============================================
                    """
                    )
                    user_data.__setitem__("password", password_hashed)
                    log.info(f"TEST DEBUG user_data: {str(user_data)}")
                    del password_hashed, password_str
                    password1 = user_data.get("password1")
                    log.info(f"TEST DEBUG password1: {str(password1)}")
                    if password1:
                        del user_data["password1"], user_data["password2"]
                except TypeError as e:
                    raise TypeError(
                        "Password should be a hashable object. " + str(e)
                    ) from e
                log.info(
                    f"TEST DEBUG BEFORE DATABASE CREATE user_data: {str(user_data)}"
                )

                user_new = PersonServiceDatabaseAdapter.save(user_data)

                log.info(
                    f"TEST DEBUG AFTER DATABASE CREATED COUNT: {str(Users.objects.count())}"
                )
                log.info(
                    f"TEST DEBUG AFTER DATABASE CREATED VALUE: {str(Users.objects.values_list("id"))}"
                )
                log.info(f"TEST DEBUG AFTER DATABASE CREATED user_new: {str(user_new)}")
                log.info(
                    f"TEST DEBUG AFTER DATABASE CREATED user_new Type: {type(user_new)}"
                )

                user_new_pydantic = [UsersPydantic.model_validate(u) for u in user_new]
                log.info(
                    f"TEST DEBUG AFTER DATABASE CREATE user_new_pydantic: {str(user_new_pydantic)}"
                )
                return user_new_pydantic[0]
            except PersonErrorImproperlyConfigured as e:
                log.info(f"TEST DEBUG PersonErrorImproperlyConfigured: {str(e)}")
                raise e
        if get_person_model_old is None:
            raise PersonErrorImproperlyConfigured("User not found.")

        try:
            is_password = PersonServiceDatabaseAdapter.is_password(user_data)
            # ============================================
            # UPDATE USER OF DATABASE
            # ============================================
            person_model_old_to_dict: dict = json.loads(
                get_person_model_old.model_dump()
            )
            if is_password:
                # ============================================
                # HASHING THE NEW USER'S PASSWORD & UPDATE
                # ============================================
                password_new_str: str = user_data.__getitem__("password")
                password_new_str: str = make_hashable(password_new_str)
                setattr(person_model_old_to_dict, "password", password_new_str)

            # exclude of fields
            forbidden_fields = {"id", "created_at", "date_joined"}
            user_data_list = list(user_data.keys())
            update_dict: dict = {
                k: user_data.pop(k)
                for k, v in person_model_old_to_dict.items()
                if k not in forbidden_fields and k in user_data_list
            }
            # ============================================
            # Here is UPDATING DATA IN DATABASE and return dictionary.
            # ============================================
            user_list = []
            try:
                Users.objects.filter(email=get_person_model_old.id).update(
                    **update_dict
                )
                u = Users.objects.get(id=get_person_model_old.id)
                user_list.append(u)
            except SynchronousOnlyOperation:

                def get_result():
                    Users.objects.filter(email=get_person_model_old.id).update(
                        **update_dict
                    )
                    u = Users.objects.get(id=get_person_model_old.id)
                    user_list.append(u)

                custom_loop = CustomizationSyncAsyncLoop()
                custom_loop.get_new_function = get_result
                wrapper = custom_loop.get_new_loop()
                thread = Thread(target=wrapper)
                thread.start()
                thread.join(timeout=8)
                logging.debug(f"Thread status after join(): {thread.is_alive()}")

            return (
                UsersPydantic.model_validate(user_list[0])
                if len(user_list) > 0
                else None
            )
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
