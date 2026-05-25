# __tests__/tests_services/test_user_service_adapter.py:1
import json
import logging

import pytest

from __tests__.fixtures.fixture_mock_patch import (
    mock_database_get_user_model,
    mock_users_database,
)
from persons.interfaces import UsersPydantic

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

    def test_is_email(self, mock_users_database ):
        # PATH: persons.adapters.person_service_adapter.PersonServiceAdapter.is_email
        from persons.adapters import PersonServiceAdapter

        # --------------------
        person = PersonServiceAdapter()
        result_email: bool = person.is_email("premium25@example.com")

        assert result_email is not None
        assert result_email is False


    def test_create_user(self, mock_users_database ):
        """
        This is a test of the create_or_update_in_database method
        PATH: persons.adapters.person_service_adapter.PersonServiceAdapter.create_or_update_in_database
        :param mock_users_database: It is the mock-Users database model. All content of the mock database at the JSON-str
        :return: void
        """

        from __tests__.fixtures.mock_function import get_file
        from persons.adapters import PersonServiceAdapter
        mock_db_json_str: str = get_file()

        new_user = {
            "email": "premium25@example.com",
            "first_name": "testFirstName",
            "last_name": "testLastName",
            "password": "pbkdf2_sha256$hash_admin_1",
        }
        # --------------------
        person = PersonServiceAdapter()
        result_email: bool = person.is_email("premium25@example.com")

        assert result_email is not None
        assert result_email is False

        # print("TEST DBUG BEFORE create person: " + str(person))
        mock_user_new:UsersPydantic =  person.create_or_update_in_database(user_data=new_user)

        mock_user_new_json = json.loads(mock_user_new.model_dump_json())
        assert type(mock_user_new_json) == dict

        mock_db_json_list: list[dict] = json.loads(mock_db_json_str)
        log.info(f"""\n
            # ============================================
            # TEST DEBUG THAT IS mock_db_json_list LENGTH (total moc database): {len(mock_db_json_list)}
            # THAT IS mock_db_json_list TYPE (total moc database): {type(mock_db_json_list)}
            # THAT IS mock_user_new_json (received a new single user) TYPE: {type(mock_user_new_json)}
            # THAT IS mock_user_new_json (received a new single user): {str(mock_user_new_json)}
            # ============================================
            """)
