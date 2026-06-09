"""
__test__/fixtures/fixture_django.py:1
"""
import logging
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest

from persons.views import UsersRegistrationView

log = logging.getLogger(__name__)
@pytest.fixture(scope="session")
def django_setup():
    import os

    import django

    """Однократная настройка Django для всех тестов"""
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    return True

# ============================================
# BELOW ARE DJNAGO's AUTH MODEL OF ABSTRACT USERS
# ============================================
@pytest.fixture
def mock_user_django():
    # from django.contrib.auth.models import AbstractUser
    from persons.models import Users
    log.info("""
    # ============================================
    # FIXTURE TEST"S MOCK - ONE DJNAGO's AUTH MODEL OF ABSTRACT USER
    # ============================================
    """)

    mock_user = Mock(spec=Users)

    # Обязательные поля
    mock_user.id = 1
    mock_user.username = "TestUsername"
    mock_user.email = "test_2_mail@host.ru"
    mock_user.password = "hashed_password_123"  # ← обязательное поле!

    # Опциональные поля с дефолтными значениями
    mock_user.first_name = "TestFirstName"
    mock_user.last_name = "TestLastName"
    mock_user.last_login = None  # может быть None

    # Boolean поля
    mock_user.is_active = True
    mock_user.is_staff = True
    mock_user.is_superuser = True
    mock_user.is_sent = False
    mock_user.is_verified = False  # ← добавить!

    # Другие поля
    mock_user.category = "BASE"
    mock_user.balance = 0.0
    mock_user.verification_code = None  # опционально

    # Даты/время
    now = datetime.now()
    mock_user.created_at = now
    mock_user.updated_at = now
    mock_user.date_joined = now
    return mock_user


# ELSE
def pytest_generate_tests(metafunc):
    if "users_model_data" in metafunc.fixturenames:
        generate_users(metafunc)

def generate_users(metafunc):
    if "users_model_data" in metafunc.fixturenames:
        base_time = datetime.now()
        users = [
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
        ]
        metafunc.parametrize(
            "users_model_data",
            users,
            ids=[s['email'] for s in users]
        )
