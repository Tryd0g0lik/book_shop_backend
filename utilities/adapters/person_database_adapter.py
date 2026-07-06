"""
persons/adapters/person_service_adapter.py:6

This is service for a work only with a business logic for the Users (Persons)
"""

import logging
from typing import Optional, TypeAlias, TypedDict, Union

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.db.models import Q, QuerySet

from persons.exceptions import PersonErrorImproperlyConfigured
from persons.interfaces import UsersPydantic
from project.settings import SECRET_KEY

log = logging.getLogger(__name__)
VerifyTypes: TypeAlias = Union[bytes, str]


class VerifyUserIdType(TypedDict):
    user_id: int


class VerifyUserEmailType(TypedDict):
    user_email: str


UserPointType = Union[VerifyUserIdType, VerifyUserEmailType]

# This is  names of keys of passwords.
# When we want to rewrite password us need to have "old_password" and "new_password"
password_keys = [
    "old_password",
    "new_password",
]


class PersonServiceDatabaseAdapter:
    """
    Here we have the two variables for works with the person database.
     - This service will allow us to get the one user by email or index, and update an one position from database.
        Make the check - we have a specific email/index of the person or not.
        For checking we have a two entry point. This is a 'user_id' and 'user_email'.
    """

    log_t = "[PersonServiceDatabaseAdapter]:"

    @staticmethod
    def get_user_by_id(user_id: Optional[int] = None) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        from persons.models import Users

        log.info(
            f"""
        {PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.get_user_by_id.__name__}]:
        # user_email: {user_id}
        """
        )
        try:
            if user_id is not None and isinstance(user_id, int):
                user = Users.objects.get(id=user_id)
                log.info(
                    f"""
                {PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.get_user_by_id.__name__}]:
                # user:  {str(user)}
                """
                )
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
        """
        GEt user from the database and conversion through the Pydantic
        Here we are not to use a cache
        :return None or Pydantic
        """
        from persons.models import Users

        log.info(
            f"""
        {PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.get_user_by_email.__name__}]:
        # user_email: {user_email}
        """
        )
        try:
            if user_email is not None and isinstance(user_email, str):
                user = Users.objects.get(email=user_email)
                log.info(
                    f"""
                {PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.get_user_by_email.__name__}]:
                # user: {str(user)}
                """
                )
                user_validated = UsersPydantic.model_validate(user)
                log.info(
                    f"""
                {PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.get_user_by_email.__name__}]:
                # user_validated: {str(user_validated)}
                """
                )
                return user_validated
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

        log.info(
            f"""
        {PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.search_by_email.__name__}]:
        # user_email: {user_email}
        """
        )
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
        """
        Save data users by email
        Creates new user or updating an exists data.
        Cache does not use, here it works directly with database.
        :param dict user_dict: Example '{"id": < USER_ID >, .... }'
        :return  list[UsersPydantic]: [...view]
        """
        from persons.models import Users

        user: Optional[Users] = None
        id_: Optional[int] = user_dict.get("id", None)
        if id_ is not None:
            # User exists by ID
            user_queryset = Users.objects.filter(id=id_)
            if not user_queryset.exists():
                log_t = (
                    PersonServiceDatabaseAdapter.log_t[:-1]
                    + f"[{PersonServiceDatabaseAdapter.save.__name__}]: Something what wrong! \
{PersonServiceDatabaseAdapter.save.__name__}: Data don't update in database!"
                )
                raise PersonErrorImproperlyConfigured(log_t)
            user_queryset.update(**user_dict)
        else:
            try:
                user_new: Users = Users.objects.create(**user_dict)
                id_ = user_new.id
            except Exception as e:
                log_t = (
                    PersonServiceDatabaseAdapter.log_t[:-1]
                    + f"[{PersonServiceDatabaseAdapter.save.__name__}]: {e.args[0] if e.args else str(e)}"
                )
                raise PersonErrorImproperlyConfigured(log_t) from e

        try:
            user = Users.objects.filter(id=id_).first()
            return [UsersPydantic.model_validate(user)]

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

        try:
            Users.objects.get(email=user_email)

            return True
        except Exception as e:
            log_t = (
                PersonServiceDatabaseAdapter.log_t[:-1]
                + f"[{PersonServiceDatabaseAdapter.is_email.__name__}]: {e.args[0] if e.args else str(e)}"
            )
            log.error(log_t)
            return False

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

            return (
                True if bool_list is not None and bool_list.count(True) == 2 else False
            )
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
        from persons.models import Users

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
        queryset_fisrt = queryset.first()
        setattr(queryset_fisrt, "password", new_passw_hash)
        queryset_fisrt.save()
        return True

    @staticmethod
    def update_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
    ) -> Optional[dict]:
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

        It's working  direct with database.
        :param user_data: Required. Dictionary with fields which we want to update. If we are wanted re-write the password
        :param user_id: Required 'user_id' or 'user_email'. User ID (optional)
        :param user_email: Required ''user_email' or 'user_id.  User email (optional)

        return: User's dict without secret data. THis is without: password and code varification.
        """
        from django.contrib.auth.models import Group

        from persons.models import Users

        if not user_data or (user_id is None and user_email is None):
            raise PersonErrorImproperlyConfigured(
                f"{PersonServiceDatabaseAdapter.log_t[:-1]}\
            [{PersonServiceDatabaseAdapter.update_in_database.__name__}]: User not found."
            )

        log.info("# Full Person's data from database")
        query_set_object: Optional[QuerySet[Users]] = None
        if user_id is not None:
            log.info("# USER ID")
            try:
                query_set_object = Users.objects.filter(id=user_id)
            except PersonErrorImproperlyConfigured as e:
                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        elif user_email is not None:
            log.info("# USER EMAIL")
            try:
                query_set_object = Users.objects.filter(email=user_email)
            except PersonErrorImproperlyConfigured as e:
                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        query_object_first = query_set_object.first()
        log.info("# WHAT WE RECEIVED FROM DATABASE")
        if query_object_first is None:
            raise PersonErrorImproperlyConfigured(
                f"{PersonServiceDatabaseAdapter.log_t[:-1]}\
            [{PersonServiceDatabaseAdapter.update_in_database.__name__}]: User not found."
            )
        try:

            log.info("# CHECKING DATA ON THE SECRET DATA & UPDATE")
            forbidden_fields = [
                "id",
                "created_at",
                "date_joined",
                "category",
                "password",
            ]
            is_password = PersonServiceDatabaseAdapter.is_password(user_data)
            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.update_in_database.__name__}]:
            # ============================================
            # FILTER OF DATA BEFORE UPDATE DATA
            # Clean data - without: id, password*, varification_code.
            # New user data: {user_data}
            # is_password: {is_password}
            # ============================================"""
            )
            update_dict: dict = {
                k: user_data.get(k)
                for k, _ in user_data.items()
                if k not in forbidden_fields
            }
            # ---- CATEGORY
            if "category" in user_data:
                query_object_first.groups.clear()
                category_str: str = user_data.get("category")

                for item in list(category_str.split(", ")):
                    group = Group.objects.filter(name=item.title())
                    if group.exists():
                        u = group.first()
                        query_object_first.groups.add(u.id)
            # ----

            for k, v in update_dict.items():
                setattr(query_object_first, k, v)
                query_object_first.save()
            # ---- PASSWORD
            if is_password:
                log.info(
                    f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.update_in_database.__name__}]:
                # ============================================
                # BEFORE CHANGING THE PASSWORD IN DATABASE 2
                #  Before checking password
                # ============================================"""
                )
                new_password = user_data.get("new_password")
                query_object_first.set_password(new_password)
                query_object_first.save()
                log.info(
                    f"""{PersonServiceDatabaseAdapter.log_t[:-1]}\
                [{PersonServiceDatabaseAdapter.update_in_database.__name__}]: Password's events is all successful!"""
                )

            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.update_in_database.__name__}]:
            # ============================================
            # AFTER FIRST.
            # queryset_updated: {query_object_first}
            # ============================================
            """
            )
            queryset_valid = UsersPydantic.model_validate(
                query_object_first
            ).to_public_dict()
            log.info(
                f"""{PersonServiceDatabaseAdapter.log_t[:-1]}[{PersonServiceDatabaseAdapter.update_in_database.__name__}]:
            # ============================================
            # AFTER UPDATE ALL DATA IN DATABASE.
            # new data of user ID: {queryset_valid["id"]}
            # updated_user: {str(queryset_valid)}
            # ============================================
            """
            )
            return queryset_valid
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
