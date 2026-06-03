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
    def test_something(self, new_users_registration):
        """
        The goal of test - create the new data of real-database,
        :param new_users_registration: It is parametrization of test.
        :param mocker:
        :return: Assert what database will be containing two lines. Contain the email = admin@example.com and moderator@example.com
        """
        log.info(f"TEST DEBUG EMAIL: {str(new_users_registration["email"])}")
        test_create_or_update_in_database: PersonServiceDatabaseAdapterInitialize = PersonServiceDatabaseAdapter.create_or_update_in_database
        del new_users_registration['check_user']
        test_create_or_update_in_database(new_users_registration)
        assert Users.objects.filter(email=new_users_registration["email"]).exists()
