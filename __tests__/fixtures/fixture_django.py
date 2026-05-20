"""
__test__/fixtures/fixture_django.py:1
"""
import logging
from datetime import datetime
from unittest.mock import Mock

import pytest

log = logging.getLogger(__name__)
@pytest.fixture(scope="session")
def django_setup():
    import os

    import django

    """Однократная настройка Django для всех тестов"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    return True

@pytest.fixture
def mock_user_django():
    log.info("""
    # ============================================
    # FIXTURE TEST"S MOCK
    # ============================================
    """)
    # mock_user = Mock()
    # mock_user.id = 1
    # mock_user.email = "test_2_mail@host.ru"
    # mock_user.username = "TestUsername"
    # mock_user.first_name = "TestFirstName"
    # mock_user.last_name = "TestLastName"
    # mock_user.is_active = True
    # mock_user.is_staff = True
    # mock_user.is_superuser = True
    # mock_user.category = "BASE"
    # mock_user.created_at = datetime.now()
    # mock_user.updated_at = datetime.now()
    # mock_user.date_joined = datetime.now()
    mock_user = Mock()

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
    mock_user.is_sent = False  # ← добавить!
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

@pytest.fixture
def mock_pydantic_user(mock_user_django):
    from persons.interfaces import UsersPydantic
    log.info("""
        # ============================================
        # FIXTURE TEST"S MOCK OF UsersPydantic.model_validate()
        # ============================================
        """)
    user_data = {
        "id": mock_user_django.id,
        "username": mock_user_django.username,
        "email": mock_user_django.email,
        "password": mock_user_django.password,
        "first_name": mock_user_django.first_name,
        "last_name": mock_user_django.last_name,
        "last_login": mock_user_django.last_login,
        "is_active": mock_user_django.is_active,
        "is_staff": mock_user_django.is_staff,
        "is_superuser": mock_user_django.is_superuser,
        "is_sent": mock_user_django.is_sent,
        "is_verified": mock_user_django.is_verified,
        "category": mock_user_django.category,
        "balance": mock_user_django.balance,
        "verification_code": mock_user_django.verification_code,
        "created_at": mock_user_django.created_at,
        "updated_at": mock_user_django.updated_at,
        "date_joined": mock_user_django.date_joined,
    }
    return UsersPydantic.model_validate(user_data)
