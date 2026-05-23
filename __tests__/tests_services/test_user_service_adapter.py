# __tests__/tests_services/test_user_service_adapter.py:1
import json
import logging

import pytest
from playwright.sync_api import expect

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import mock_database_get_user_model

log = logging.getLogger(__name__)


class TestUserServiceAdapter:

    @pytest.mark.parametrize("userId, userEm, expect", [
        (4, "moderator@example.com", True),
        (7, "john.doe@example.com", True),
        (7, "john.doe@example.com", False)
    ])
    def test_get_user_by_id(self,userId, userEm,expect, mock_database_get_user_model):
        """
        :param userId:
        :param userEm:
        :param expect:
        :param mock_database_get_user_model: This is the mock-Users database model. All content  of the mock database
            to the '__tests__.fixtures.fixture_django.pytest_generate_tests'
        :return:
        """
        from persons.adapters import PersonServiceAdapter

        mock_user = mock_database_get_user_model
        if mock_user in [userId]:
            result = PersonServiceAdapter.get_user_by_id(user_id=userId)

            assert result is not None if expect else result is None
            if expect and result is not None:
                result_json: dict = json.loads(result.model_dump_json())
                assert type(result_json) == dict
                em = result_json.__getitem__("email")
                ind = result_json.__getitem__("id")
                assert em is not None
                assert ind is not None
                print("TEST DEBUG test_get_user_by_id Type:%s & STR: %s" % (type(result_json), str(result_json)[:25]))
                assert ind == userId
                assert em == userEm
