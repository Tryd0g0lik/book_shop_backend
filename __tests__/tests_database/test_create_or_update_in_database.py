import logging
import unittest

import pytest
from colorful.terminal import TRUE_COLORS

from __tests__.fixtures.fixture_django2 import pytest_generate_tests
from persons.adapters import PersonServiceDatabaseAdapter
from persons.interfaces import (
    PersonServiceDatabaseAdapter as PersonServiceDatabaseAdapterInitialize,
)
from persons.models import Users

log = logging.getLogger(__name__)

# pytest_generate_tests_regisration

class TestCreateOrUpdateInDatabase:

    @pytest.mark.django_db()
    def test_something(self,):
        """
        The goal of test - create the new data of real-database,
        :param new_users_registration: It is parametrization of test.
        :param mocker:
        :return: Assert what database will be containing two lines. Contain the email = admin@example.com and moderator@example.com
        """
        new_users_registration = {"is_superuser": False,
        "username": "staff_moderator",
        "first_name": "Moderator",
        "last_name": "Staff",
        "email": "moderator@example.com",
        "is_staff": True,
        "is_active": True,
        "category": "STAFF",
        "password": "pbkdf2_sha256$hash_staff_2",
        "is_sent": True,
        "is_verified": True,
        "verification_code": None,}
        log.info(f"TEST DEBUG EMAIL: {str(new_users_registration["email"])}")
        test_create_or_update_in_database: PersonServiceDatabaseAdapterInitialize = PersonServiceDatabaseAdapter.create_or_update_in_database

        Users.objects.create(**new_users_registration)
        old_email: str = new_users_registration['email']
        new_users_registration["email"] = 'new@email.com'
        test_create_or_update_in_database(user_data=new_users_registration, user_email=old_email)
        assert Users.objects.filter(email='new@email.com').exists()
