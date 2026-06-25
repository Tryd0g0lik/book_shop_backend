# __tests__/fixtures/mock_function.py:1
import io
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from persons.interfaces import UsersPydantic
from project.settings_conf.settings_db import DATABASES

base_time = datetime.now()
log = logging.getLogger(__name__)


# ============================================
# MOCK SUB PERSON CLASS
# ============================================
def __get_cache_staticmethod(value: str = None) -> Optional[list[bytes] | dict]:
    """It's direct work with the Redis's cache"""
    from persons.services import CacheManager

    log.info("""
            # ============================================
            # Mock __get_cache_staticmethod vs SubPerson.__get_cache
            # ============================================
            """)
    cachemanager_test = CacheManager()

    # value_of_cache: Optional[bytes] = None
    value_of_cache: Optional[list | dict] = []
    log.info(f"[Mock __get_cache.CacheManager ]: Before Value: {str(value)}")
    cachemanager_test.get(key=value, collection=value_of_cache, exat=86400)

    log.info(f"[Mock __get_cache.CacheManager ]: After result {str(value_of_cache)}")
    return value_of_cache


def is_person_velidator(mock_pydantic_user):
    def wrapper(value=None):

        log.info("""
            # ============================================
            # Mock is_person_velidator vs SubPerson._is_person
            # ============================================
            """)
        if mock_pydantic_user is None:
            raise TypeError(f"Expected UsersPydantic, got {type(mock_pydantic_user)}")
        return True

    return wrapper


# ============================================
# MOCK PERSON SERVICE ADAPTER
# ============================================
def database_service_get_user_by_email(mock_pydantic_user):
    def wrapper(user_email=None):
        log.info("""
            # ============================================
            # Mock database_service_get_user_by_email vs PersonServiceAdapter.get_user_by_emai
            # ============================================
            """)
        return mock_pydantic_user

    return wrapper()


def database_service_get_user_by_id(mock_pydantic_user):
    def wrapper(user_id=None):
        log.info("""
            # ============================================
            # Mock database_service_get_user_by_id vs PersonServiceAdapter.get_user_by_id
            # ============================================
            """)
        return mock_pydantic_user

    return wrapper()


# ============================================
# MOCK DATABASE IN FILE
# ============================================
DATABASES_FILE_NAME = "mock_user_database.txt"

# class MockDatabaseServiceFile:
#     def __init__(self,):
#         self.io_file:Optional[io.StringIO] = None
#
#     def is_file(self) -> bool:
#         try:
#             self.io_file = io.StringIO()
#             self.io_file.write(
#
#     )
#             return True
#         except Exception as e:
#             print(f"File io_file failed {e.args}")
#             return False


# def get_file(self):
#     fil = self.io_file.getvalue()
#     fil_json = json.loads(fil)
#     print(f"{self.get_file.__name__} Type: {list(fil_json)[:3]}")
#     return fil_json
def datetime_serialize(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__}  is not JSON serializable")


def get_file():

    file_str = json.dumps(
        [
            {
                "id": 1,
                "last_login": base_time - timedelta(days=1),
                "is_superuser": True,
                "username": "admin_super",
                "first_name": "Admin",
                "last_name": "Supervisor",
                "email": "admin@example.com",
                "is_staff": True,
                "is_active": True,
                "date_joined": base_time - timedelta(days=365),
                "category": "ADMIN",
                "password": "pbkdf2_sha256$hash_admin_1",
                "is_sent": True,
                "is_verified": True,
                "verification_code": "admin_verification_code_123",
                "balance": 0.0,
                "created_at": base_time - timedelta(days=365),
                "updated_at": base_time - timedelta(days=1),
            },
            {
                "id": 2,
                "last_login": base_time - timedelta(hours=12),
                "is_superuser": False,
                "username": "staff_moderator",
                "first_name": "Moderator",
                "last_name": "Staff",
                "email": "moderator@example.com",
                "is_staff": True,
                "is_active": True,
                "date_joined": base_time - timedelta(days=180),
                "category": "STAFF",
                "password": "pbkdf2_sha256$hash_staff_2",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 0.0,
                "created_at": base_time - timedelta(days=180),
                "updated_at": base_time - timedelta(hours=12),
            },
            {
                "id": 3,
                "last_login": base_time - timedelta(days=3),
                "is_superuser": False,
                "username": "premium_user",
                "first_name": "Premium",
                "last_name": "Customer",
                "email": "premium@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": base_time - timedelta(days=90),
                "category": "PREMIUM",
                "password": "pbkdf2_sha256$hash_premium_3",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 1500.50,
                "created_at": base_time - timedelta(days=90),
                "updated_at": base_time - timedelta(days=3),
            },
            {
                "id": 4,
                "last_login": None,
                "is_superuser": False,
                "username": "new_user_unverified",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": base_time - timedelta(days=1),
                "category": "BASE",
                "password": "pbkdf2_sha256$hash_new_4",
                "is_sent": True,
                "is_verified": False,
                "verification_code": f"verify_{uuid4().hex[:32]}",
                "balance": 0.0,
                "created_at": base_time - timedelta(days=1),
                "updated_at": base_time - timedelta(days=1),
            },
            {
                "id": 5,
                "last_login": None,
                "is_superuser": False,
                "username": "inactive_user",
                "first_name": "Inactive",
                "last_name": "Account",
                "email": "inactive@example.com",
                "is_staff": False,
                "is_active": False,
                "date_joined": base_time - timedelta(days=60),
                "category": "BASE",
                "password": "pbkdf2_sha256$hash_inactive_5",
                "is_sent": False,
                "is_verified": False,
                "verification_code": None,
                "balance": 0.0,
                "created_at": base_time - timedelta(days=60),
                "updated_at": base_time - timedelta(days=30),
            },
            {
                "id": 6,
                "last_login": base_time - timedelta(hours=2),
                "is_superuser": False,
                "username": "rich_customer",
                "first_name": "Rich",
                "last_name": "Client",
                "email": "rich@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": base_time - timedelta(days=300),
                "category": "VIP",
                "password": "pbkdf2_sha256$hash_rich_6",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 10000.00,
                "created_at": base_time - timedelta(days=300),
                "updated_at": base_time - timedelta(hours=2),
            },
            {
                "id": 7,
                "last_login": base_time - timedelta(days=7),
                "is_superuser": False,
                "username": "regular_john",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": base_time - timedelta(days=120),
                "category": "BASE",
                "password": "pbkdf2_sha256$hash_john_7",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 250.75,
                "created_at": base_time - timedelta(days=120),
                "updated_at": base_time - timedelta(days=7),
            },
            {
                "id": 8,
                "last_login": None,
                "is_superuser": False,
                "username": "pending_activation",
                "first_name": "Pending",
                "last_name": "User",
                "email": "pending@example.com",
                "is_staff": False,
                "is_active": False,
                "date_joined": base_time - timedelta(days=0, hours=2),
                "category": "BASE",
                "password": "pbkdf2_sha256$hash_pending_8",
                "is_sent": True,
                "is_verified": False,
                "verification_code": f"activate_{uuid4().hex[:24]}",
                "balance": 0.0,
                "created_at": base_time - timedelta(days=0, hours=2),
                "updated_at": base_time - timedelta(days=0, hours=2),
            },
            {
                "id": 9,
                "last_login": base_time - timedelta(days=10),
                "is_superuser": False,
                "username": "support_agent",
                "first_name": "Support",
                "last_name": "Agent",
                "email": "support@example.com",
                "is_staff": True,
                "is_active": True,
                "date_joined": base_time - timedelta(days=200),
                "category": "SUPPORT",
                "password": "pbkdf2_sha256$hash_support_9",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 0.0,
                "created_at": base_time - timedelta(days=200),
                "updated_at": base_time - timedelta(days=10),
            },
            {
                "id": 10,
                "last_login": base_time - timedelta(days=0, hours=6),
                "is_superuser": False,
                "username": "test_user_10",
                "first_name": "Test",
                "last_name": "UserTen",
                "email": "test10@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": base_time - timedelta(days=45),
                "category": "BASE",
                "password": "pbkdf2_sha256$hash_test10",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 50.00,
                "created_at": base_time - timedelta(days=45),
                "updated_at": base_time - timedelta(days=0, hours=6),
            },
        ],
        default=datetime_serialize,
    )
    return file_str
    # def close_file(self) -> bool:
    #     try:
    #         self.io_file.close()
    #         return True
    #     except Exception:
    #         return False


def get_one_user(*args, **kwargs) -> Optional[dict]:
    print("TEST DBUG IN: " + str(args) + " & " + str(type(kwargs)))
    # Достаём базу данных из kwargs
    if "database" not in kwargs:
        # Если база не передана, возможно, это ошибка в тесте
        return None
    mock_database: list[dict] = kwargs["database"]

    # 1. Пробуем найти email в ключевых аргументах (КРИТИЧЕСКИ ВАЖНО)
    email_to_find = kwargs.get("email")

    # 2. Если в ключевых нет, пробуем взять из позиционных (для совместимости)
    if email_to_find is None and len(args) > 0:
        email_to_find = args[0]

    print(f"TEST DEBUG USER_LIS BEFORE EMAIL: {email_to_find}")
    ind: Optional[int] = None
    # ind_list = [i - 1 if i > 0 else 0 for i in args]
    email_list = list(email_to_find)
    user_lis: list[dict] = [
        one_use for one_use in mock_database if one_use["email"] == email_to_find
    ]
    print("TEST DEBUG USER_LIS: " + str(user_lis))
    if len(user_lis) > 0:
        return user_lis[0]
    else:
        raise ValueError("EMail not found")


def save_one_user(*args: list[dict], **kwargs: dict) -> UsersPydantic:
    """

    :param (list[dict],) args: This is a list old the database's data
    :param dict kwargs: This is a dict with new data from variables: 'username', 'email', 'password', 'first_name', 'last_name',
        'last_login', 'is_active', 'is_staff', 'is_superuser', 'is_sent',
        'is_verified', 'category', 'balance', 'verification_code',
    :return: list[dict]  new data
    """
    from datetime import datetime, timedelta

    base_time = datetime.now()
    user_dict: dict = kwargs
    get_list: list[dict] = []
    for one_list in args:
        get_list.extend(one_list)

    template_new_user: dict = {
        "id": len(get_list) + 1,
        "last_login": None,
        "is_superuser": False,
        "username": "test_user_10",
        "first_name": "Test",
        "last_name": "UserTen",
        "email": f"test{len(get_list)}@example.com",
        "is_staff": False,
        "is_active": True,
        "date_joined": base_time,
        "category": "BASE",
        "password": f"pbkdf2_sha{len(get_list)}6$hash_test10",
        "is_sent": True,
        "is_verified": True,
        "verification_code": None,
        "balance": 0.00,
        "created_at": base_time,
        "updated_at": base_time,
    }
    # Create a new user
    template_keys = list(template_new_user.keys())
    [
        template_new_user.__setitem__(k, v)
        for k, v in user_dict.items()
        if k in template_keys
    ]

    # Returning the update database
    get_list.append(template_new_user)
    new_user = UsersPydantic(**template_new_user)
    log.info(f"""\n
       # ============================================
       # TEST DEBUG FIXTURE save_one_user CREATING OF USER
       # - template_keys LEN: {len(template_keys)}
       # - template_new_user NEW: {str(template_new_user)}
       # - get_list ( mock db) LEN: {len(get_list)}
       # - get_list ( mock db) TYPE: {type(get_list)}
       # ============================================
       """)
    return new_user
