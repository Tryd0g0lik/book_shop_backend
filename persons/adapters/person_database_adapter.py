"""
persons/adapters/person_service_adapter.py:6

This is service for a work only with a business logic for the Users (Persons)
"""

import json
import logging
from typing import Optional, TypeAlias, TypedDict, Union

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.db.models import Q
from django.utils.hashable import make_hashable
from zope.interface.common import optional

from persons.exceptions import PersonErrorImproperlyConfigured
from persons.interfaces import UsersPydantic
from persons.models import Users
from project.settings import SECRET_KEY
from project.settings_conf.settings_env import APP_MINIMUM_PASSWORD_LENGTH

log = logging.getLogger(__name__)
VerifyTypes: TypeAlias = Union[bytes, str]


class VerifyUserIdType(TypedDict):
    user_id: int


class VerifyUserEmailType(TypedDict):
    user_email: str


UserPointType = Union[VerifyUserIdType, VerifyUserEmailType]

# This is  names of keys of passwords.
# When we want to rewrite password us need to have "old_password" and "new_password"
password_keys = ["old_password", "new_password"]


class PersonServiceDatabaseAdapter:
    """
    Here we have the two variables for works with the person database.
     - This service will allow us to get the one user by email or index, or create_or_update  one position from database.
        Make the check - we have a specific email/index of the person or not.
        For checking we have a two entry point. This is a 'user_id' and 'user_email'.
    """

    log_t = "[PersonServiceDatabaseAdapter]:"
    # def __new__(cls, *args, **kwargs):
    #     initionally = super().__new__(cls, *args, **kwargs)
    #     initionally.log_t = PersonServiceDatabaseAdapter.__class__.__name__
    #     return initionally

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
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[PersonServiceDatabaseAdapter.get_user_by_id.__name__]: {e.args[0] if e.args else str(e)}"
            )
            raise PersonErrorImproperlyConfigured(log_t) from e

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
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.get_user_by_email.__name__}]: {e.args[0] if e.args else str(e)}"
            )
            raise PersonErrorImproperlyConfigured(log_t) from e
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
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.search_by_email.__name__}]: {e.args[0] if e.args else str(e)}"
            )
            raise PersonErrorImproperlyConfigured(log_t) from e

    @staticmethod
    def save(user_dict: dict) -> list[UsersPydantic]:
        """Save data users by email"""
        from persons.models import Users

        user_list = []
        try:
            user = Users.objects.create(**user_dict)
            user_list.append(user)

            return (
                [UsersPydantic.model_validate(user_list[0])]
                if len(user_list) > 0
                else []
            )
        except Exception as e:
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.save.__name__}]: {e.args[0] if e.args else str(e)}"
            )
            raise PersonErrorImproperlyConfigured(log_t) from e

    @staticmethod
    def is_email(user_email: str) -> bool:
        """Search users by email"""
        from persons.models import Users
        from persons.services import CustomizationSyncAsyncLoop

        try:
            print(f"\n ------------------ \n DEBUG BEFORE. email:  {str(user_email)}")
            test_result = Users.objects.get(email=user_email)

            return True if test_result is not None else False
        except Exception as e:
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.is_email.__name__}]: {e.args[0] if e.args else str(e)}"
            )

            raise PersonErrorImproperlyConfigured(log_t) from e

    @staticmethod
    def is_password(user_data: dict) -> bool:
        """
        This method only check - The 'user_data' contain anything from  set password_keys (above) or not.
        :return True if it is containing or False
        """
        try:
            bool_list = [
                True if k in password_keys else False for k, _ in user_data.items()
            ]

            return bool_list[0]
        except Exception as e:
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.is_password.__name__}]: {e.args[0] if e.args else str(e)}"
            )
            raise PersonErrorImproperlyConfigured(log_t) from e

    @staticmethod
    def hashes_password(password: Optional[str]) -> Optional[str]:
        """
        The 'user_data' can contain not only the key 'password' also 'password1' + 'password2' (without 'password').
        Us need to find an existing key then convert it to the hash.

        Secure password hashing using the PBKDF2 algorithm (recommended)
        Configured to use PBKDF2 + HMAC + SHA256.
        The result is a 64 byte binary string. Iterations may be changed
        safely but you must rename the algorithm if you change SHA256.
        Current algorithm is: 'pbkdf2_sha256'
        Template is : "%s$%d$%s$%s" (algorithm,iterations, salt, hash )

        If 'user_data' AND 'password' is None means returning a mistake.
        :param str password: It is original password from form.
        :return: str|None or mistake 'PersonErrorImproperlyConfigured'
        """
        password_str: Optional[str] = None
        if password is None:
            raise PersonErrorImproperlyConfigured(
                f"[{PersonServiceDatabaseAdapter.hashes_password.__name__}]: \
            Data is not found,"
            )

        if password is not None:
            password_str = password[:]
        try:
            # ============================================
            # HASHING A USER'S PASSWORD
            # ============================================
            make_hash = PBKDF2PasswordHasher()
            password_hashed: str = make_hash.encode(
                password=password_str, salt=SECRET_KEY[:25]
            )
            log.info(
                f"""\n\t
            # ============================================
            # DEBUG HASH {PersonServiceDatabaseAdapter.hashes_password.__name__}:
            # password_hashed: {password_hashed}
            # ============================================
            """
            )
            return password_hashed
        except TypeError as e:
            log_T = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.hashes_password.__name__}]:"
            )
            raise PersonErrorImproperlyConfigured(
                log_T + "Password should be a hashable string. " + e.args[0]
                if e.args
                else str(e)
            ) from e
        except Exception as e:
            log_T = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.hashes_password.__name__}]:"
            )
            raise PersonErrorImproperlyConfigured(
                log_T + "Password should be a hashable string. " + e.args[0]
                if e.args
                else str(e)
            ) from e

    @staticmethod
    def change_password(
        old_password: str, new_password: str, **kwargs: UserPointType
    ) -> bool:
        """
        This method is only checker.
        It does not to make changes in the database.
        :param str old_password: Required. It is old the original user's password row from form.
        :param str new_password:  Required. It is new the original user's password row from form. \
        :param UserPointType kwargs: Required. '{user_id: str}' or '{user_email: str}'
        :return: if 'old_password' equal to 'new_password' mean a new password will be saving in database then will be returning a True, or mistake 'PersonErrorImproperlyConfigured'.
        """
        keys = list(kwargs.keys())
        keys_size = len(keys)
        if (
            not isinstance(old_password, str)
            or not isinstance(new_password, str)
            or keys_size == 0
        ):
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.change_password.__name__}]:"
            )
            raise PersonErrorImproperlyConfigured(
                log_t + " Data Type Values is not corrected."
            )

        old_passw_hash = PersonServiceDatabaseAdapter.hashes_password(
            password=old_password
        )
        new_passw_hash = PersonServiceDatabaseAdapter.hashes_password(
            password=new_password
        )

        # user = Users.objects.get(id=kwargs.get("user_id")) if "user_id" in keys \
        #     else Users.objects.get(email=kwargs.get("user_email"))

        queryset = Users.objects.filter(
            Q(id=kwargs.get("user_id")) | Q(email=kwargs.get("user_email")),
            password=old_passw_hash,
        )
        if not queryset.exists():
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.change_password.__name__}]:"
            )
            raise PersonErrorImproperlyConfigured(
                log_t
                + " There are not anyone user which  will be containing a similar password with 'old_password'."
            )
        queryset.update(password=new_passw_hash)
        return True

    @staticmethod
    def create_or_update_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
    ) -> dict:
        """
        TODO: user_data - обязательный атрибут.
            Если user_id или user_email не равно None. Значит данные на обновление,
            Если user_id или user_email не равно None:
             - Создаю нового подльзователя смотрим в кеше по ключу: user:pending:login:<EMAIL> - Проверить работу с кешем .
             Главное В этом файле работаю только с базой данных
             &
             Тут нет проверки паролей. Сравнение паролей - нового и старого хешированного должно проходить вне этого метода
             &
             Сюда пароль поступает в родительском состоянии . Тут хешируется перед сохранением.


        :param user_data: Dictionary with fields which we want to update. If we are wanted re-write the password
        :param user_id: User ID (optional)
        :param user_email: User email (optional)

        return: User's dict without secret data. These are - password and code varification.
        """
        from persons.models import Users

        # Full Person's data from database
        get_person_pydantic_old: Optional[UsersPydantic] = None

        if user_id is not None:
            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]:
            # ============================================
            # UPDATE USER FROM  DATABASE BY user_id
            # ============================================
            """
            )
            try:
                get_person_pydantic_old = PersonServiceDatabaseAdapter.get_user_by_id(
                    user_id
                )
            except PersonErrorImproperlyConfigured as e:

                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        elif user_email is not None:
            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]:
            # ============================================
            # UPDATE USER FROM  DATABASE BY user_email
            # ============================================"""
            )
            try:
                get_person_pydantic_old = (
                    PersonServiceDatabaseAdapter.get_user_by_email(user_email)
                )
            except PersonErrorImproperlyConfigured as e:
                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

        if get_person_pydantic_old is None:
            raise PersonErrorImproperlyConfigured("User not found.")

        try:

            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]:
            # ============================================
            # UPDATE USER OF DATABASE
            # ============================================"""
            )
            person_model_old_to_dict: dict = json.loads(
                get_person_pydantic_old.model_dump()
            )

            log.info(
                f"{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]: # exclude of fields"
            )
            forbidden_fields = {"id", "created_at", "date_joined"}
            user_data_list = list(user_data.keys())
            update_dict: dict = {
                k: user_data.pop(k)
                for k, v in person_model_old_to_dict.items()
                if k not in forbidden_fields and k in user_data_list
            }
            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]:
            # ============================================
            # BEFORE UPDATE DATA IN DATABASE.
            # ============================================
            """
            )
            Users.objects.filter(email=get_person_pydantic_old.id).update(**update_dict)
            updated_user = Users.objects.get(id=get_person_pydantic_old.id)
            is_password = PersonServiceDatabaseAdapter.is_password(user_data)
            if is_password:
                log.info(
                    f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]:
                # ============================================
                # BEFORE CHANGING THE PASSWORD IN DATABASE
                #  Before checking password
                # ============================================"""
                )
                passw_keys: list = [
                    k for k, _ in user_data.items() if k in password_keys
                ]
                passw_len: int = len(passw_keys)
                if passw_len < 2:
                    log.info(
                        f"""{PersonServiceDatabaseAdapter.log_t[:-1]}\
                    [{PersonServiceDatabaseAdapter.is_password.__name__}]:
                    # ============================================
                    # Password's events is all successful!
                    # It not been changed in database.
                    # PASSWORD NOT FOUND TO SET '["old_password", "new_password"]'. Check the name of password's key
                    # ============================================
"""
                    )
                else:
                    old_password = user_data.get("old_password")
                    new_password = user_data.get("new_password")
                    kwargs = {"user_id": get_person_pydantic_old.id}
                    PersonServiceDatabaseAdapter.change_password(
                        old_password, new_password, **kwargs
                    )
                    log.info(
                        f"""{PersonServiceDatabaseAdapter.log_t[:-1]}\
                    [{PersonServiceDatabaseAdapter.is_password.__name__}]: Password's events is all successful!"""
                    )
            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.is_password.__name__}]:
            # ============================================
            # AFTER UPDATE ALL DATA IN DATABASE.
            # ============================================
            """
            )
            valid_user = UsersPydantic.model_validate(updated_user)
            return valid_user.to_dict_without_secret_data()
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    # @staticmethod
    # def create_or_update_in_database(
    #     user_data: dict,
    #     user_id: Optional[int] = None,
    #     user_email: Optional[str] = None,
    # ) -> UsersPydantic:
    #     """
    #     TODO: user_data - обязательный атрибут.
    #         Если user_id или user_email не равно None. Значит данные на обновление,
    #         Если user_id или user_email не равно None:
    #          - Создаю нового подльзователя смотрим в кеше по ключу: user:pending:login:<EMAIL> - Проверить работу с кешем .
    #          Главно В этом файле работаю только с базой данных
    #          &
    #          Тут нет проверки паролей. Сравнение паролей - нового и старого хешированного должно проходить вне этого метода
    #          &
    #          Сюда пароль поступает в родительском состоянии . Тут хешируется перед сохранением.
    #
    #     Args:
    #         :param user_data: Dictionary with fields to update
    #         :param user_id: User ID (optional)
    #         :param user_email: User email (optional)
    #
    #     Returns:
    #         Updated user as Pydantic model
    #     """
    #     from persons.models import Users
    #
    #     get_person_model_old: Optional[UsersPydantic] = None
    #     em: Optional[str] = user_data.__getitem__("email")
    #
    #     if user_id is not None:
    #         # ============================================
    #         # UPDATE USER FROM  DATABASE BY user_id
    #         # ============================================
    #         try:
    #             get_person_model_old = PersonServiceDatabaseAdapter.get_user_by_id(
    #                 user_id
    #             )
    #         except PersonErrorImproperlyConfigured as e:
    #
    #             raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
    #     elif user_email is not None:
    #         # ============================================
    #         # UPDATE USER FROM  DATABASE BY user_email
    #         # ============================================
    #         try:
    #             get_person_model_old = PersonServiceDatabaseAdapter.get_user_by_email(
    #                 user_email
    #             )
    #         except PersonErrorImproperlyConfigured as e:
    #             raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
    #     #         if get_person_model_old is None and em is not None:
    #     #             # ============================================
    #     #             # CREATE NEW USER IN DATABASE
    #     #             # ============================================
    #     #
    #     #             try:
    #     #                 # is_user: bool = PersonServiceDatabaseAdapter.is_email(em)
    #     #                 # log.info(f"TEST DEBUG AFTER is_user: {str(is_user)}")
    #     #                 #
    #     #                 # if is_user:
    #     #                 #     """
    #     #                 #     This mean - user already exists.
    #     #                 #     Return error message
    #     #                 #     """
    #     # #                     raise PersonErrorImproperlyConfigured(
    #     # #                         "User already exists was founded before it. \
    #     # # Change the email address."
    #     # #                     )

    #     #                 log.info(
    #     #                     f"TEST DEBUG BEFORE DATABASE CREATE user_data: {str(user_data)}"
    #     #                 )
    #     #
    #     #                 user_new = PersonServiceDatabaseAdapter.save(user_data)
    #     #
    #     #                 log.info(f"TEST DEBUG AFTER DATABASE CREATED COUNT: {str(Users.objects.count())}")
    #     #                 log.info(f"TEST DEBUG AFTER DATABASE CREATED VALUE: {str(Users.objects.values_list("id"))}")
    #     #                 log.info(f"TEST DEBUG AFTER DATABASE CREATED user_new: {str(user_new)}")
    #     #                 log.info(f"TEST DEBUG AFTER DATABASE CREATED user_new Type: {type(user_new)}")
    #     #
    #     #                 user_new_pydantic = [UsersPydantic.model_validate(u) for u in user_new]
    #     #                 log.info(
    #     #                     f"TEST DEBUG AFTER DATABASE CREATE user_new_pydantic: {str(user_new_pydantic)}"
    #     #                 )
    #     #                 return user_new_pydantic[0]
    #     #             except PersonErrorImproperlyConfigured as e:
    #     #                 log.info(f"TEST DEBUG PersonErrorImproperlyConfigured: {str(e)}")
    #     #                 raise e
    #     if get_person_model_old is None:
    #         raise PersonErrorImproperlyConfigured("User not found.")
    #
    #     try:
    #         is_password = PersonServiceDatabaseAdapter.is_password(user_data)
    #         # ============================================
    #         # UPDATE USER OF DATABASE
    #         # ============================================
    #         person_model_old_to_dict: dict = json.loads(
    #             get_person_model_old.model_dump()
    #         )
    #         if is_password:
    #             # ============================================
    #             # HASHING THE NEW USER'S PASSWORD & UPDATE
    #             # ============================================
    #             password_new_str: str = user_data.__getitem__("password")
    #             password_new_str: str = make_hashable(password_new_str)
    #             setattr(person_model_old_to_dict, "password", password_new_str)
    #
    #         # exclude of fields
    #         forbidden_fields = {"id", "created_at", "date_joined"}
    #         user_data_list = list(user_data.keys())
    #         update_dict: dict = {
    #             k: user_data.pop(k)
    #             for k, v in person_model_old_to_dict.items()
    #             if k not in forbidden_fields and k in user_data_list
    #         }
    #         # ============================================
    #         # Here is UPDATING DATA IN DATABASE and return dictionary.
    #         # ============================================
    #         Users.objects.filter(email=get_person_model_old.id).update(**update_dict)
    #         updated_user = Users.objects.get(id=get_person_model_old.id)
    #         return UsersPydantic.model_validate(updated_user)
    #     except Exception as e:
    #         log_t = (
    #             PersonServiceDatabaseAdapter.log_t[:-1]
    #             + f"[{PersonServiceDatabaseAdapter.is_password.__name__}]: {e.args[0] if e.args else str(e)}"
    #         )
    #         raise PersonErrorImproperlyConfigured(log_t) from e
