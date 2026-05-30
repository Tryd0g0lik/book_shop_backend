import logging

import pytest

from __tests__.fixtures.fixture_django import mock_user_django

log = logging.getLogger(__name__)

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
