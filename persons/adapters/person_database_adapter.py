"""
persons/adapters/person_service_adapter.py:6

This is service for a work only with a business logic for the Users (Persons)
"""

import json
import logging
from typing import Optional

from django.utils.hashable import make_hashable

from persons.exceptions import PersonErrorImproperlyConfigured
from persons.interfaces import UsersPydantic

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

        try:
            if user_email is not None and isinstance(user_email, str):
                user = Users.objects.get(email=user_email)
                return UsersPydantic.model_validate(user)
        except Users.DoesNotExist:
            return None
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        return None

    @staticmethod
    def search_by_email(user_email: str) -> list[UsersPydantic]:
        """Search users by email"""
        from persons.models import Users

        try:
            users = Users.objects.filter(email__icontains=user_email)
            return (
                [UsersPydantic.model_validate(u) for u in users]
                if len(users) > 0
                else []
            )
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def is_email(user_email: str) -> bool:
        """Search users by email"""
        from persons.models import Users

        try:
            print(
                f"\n ------------------ \n TEST DEBUG BEFORE. email:  {str(user_email)}"
            )
            test_result = Users.objects.get(email=user_email)
            print(
                f"\n ------------------ \n\t TEST DEBUG AFTER Users.objects cycle. email:  {str(test_result)}"
            )
            return True
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
        elif em is not None:
            # ============================================
            # CREATE NEW USER IN DATABASE
            # ============================================

            try:
                is_user: bool = PersonServiceDatabaseAdapter.is_email(em)
                print(f"TEST DEBUG AFTER is_user: {str(is_user)}")

                if is_user:
                    """
                    This mean - user already exists.
                    Return error message
                    """
                    raise PersonErrorImproperlyConfigured(
                        "User already exists was founded before it. \
Change the email address."
                    )
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
                    password_hashed = make_hashable(password_str)
                    log.info(
                        f"""\n\t
                    # ============================================
                    # TEST DEBUG create_or_update_in_database
                    # That is user_data: {str(user_data)}
                    # That is the type of user_data: {type(user_data)}
                    # ============================================
                    """
                    )
                    user_data.__setitem__("password", password_hashed)
                    del password_hashed, password_str
                    password1 = user_data.get("password1")
                    if password1:
                        del user_data["password1"]
                except TypeError as e:
                    raise TypeError(
                        "Password should be a hashable object. " + str(e)
                    ) from e
                user_new = Users.objects.create(**user_data)
                return UsersPydantic.model_validate(user_new)
            except PersonErrorImproperlyConfigured as e:
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
            Users.objects.filter(email=get_person_model_old.id).update(**update_dict)
            updated_user = Users.objects.get(id=get_person_model_old.id)
            return UsersPydantic.model_validate(updated_user)
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
