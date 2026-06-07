"""
# __tests__/tests_services/test_user_service_adapter.py:1
This is a test for the PersonServiceAdapter methods.
Our goal, here is testing a logic of the body get_user_by_id (and some) and will get the data one person (from mock-database).
The data of person from the mock database.
THe method itself doesn't  check the incoming content. All checks should be above entrypoint.
THe all methods, from the PersonServiceAdapter, have a direct work wits a database (a mock database).
NOTE: THe direct work with real database is currently missing.
"""

import json
import logging

import pytest

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import (
    mock_database_get_user_model,
    mock_database_get_user_model_2,
    mock_users_database,
)
from persons.interfaces import UsersPydantic

log = logging.getLogger(__name__)


class TestUserServiceAdapter:
    # def test_get_user_by_id(self,userId, userEm,expect, mock_database_get_user_model):
    # @pytest.mark.skip("Пересмотреть логику 'mock_database_get_user_model'", )
    @pytest.mark.skip(reason="This test is skipped. Launch after data is entered in to the database")
    @pytest.mark.parametrize("userId, userEm, expect", [
        (4, "new@example.com", True),
    ])
    def test_get_user_by_id(self,userId, userEm,expect, users_model_data, mock_database_get_user_model_2):
        """

        :param int userId: Index of mock person
        :param userEm:
        :param expect:
        :param mock_database_get_user_model_2: This is the mock-Users.users.get database model.
        All content  of the mock database to the '__tests__.fixtures.fixture_django.pytest_generate_tests'
        :return:
        """
        from persons.adapters import PersonServiceDatabaseAdapter

        mock_user = users_model_data
        if mock_user["id"] in [4, 7]:
            log.info(f"""\n\t
            # ============================================
            # TEST DEBUG test_get_user_by_id BEFORE FIRST CONDITIONS:
            # - mock_user: {str(mock_user)[:25]}
            # - userId (of entrypoint): {str(userId)}
            # ============================================
            """)
            if mock_user['id'] in [userId]:
                result = PersonServiceDatabaseAdapter.get_user_by_id(user_id=userId)
                log.info(f"""\n\t
                # ============================================
                # TEST DEBUG test_get_user_by_id AFTER RESULT:
                # - result (of .get_user_by_id): {str(result)[:25]}
                # ============================================
                """)
                assert result is not None if expect else result is None
                if expect and result is not None:
                    result_json: dict = json.loads(result.model_dump_json())
                    assert type(result_json) == dict
                    keys = list(result_json.keys())
                    em = result_json.__getitem__("email") if "email" in keys else None
                    ind = result_json.__getitem__("id") if id in keys else -999
                    assert em is not None
                    assert ind is not None
                    print("TEST DEBUG test_get_user_by_id Type:%s & STR: %s" % (type(result_json), str(result_json)[:25]))
                    assert ind == userId
                    assert em == userEm

    def test_is_email(self, mock_users_database ):
        # PATH: persons.adapters.person_dabase_adapter.PersonServiceDatabaseAdapter.is_email
        from persons.adapters import PersonServiceDatabaseAdapter

        # --------------------
        person = PersonServiceDatabaseAdapter()
        result_email: bool = person.is_email("premium25@example.com")

        assert result_email is not None
        assert result_email is False


    # def test_create_user(self, mock_users_database ):
    #     """
    #     This is a test of the 'update_in_database' method.
    #     This test is testing that we send data to the 'PersonServiceAdapter.update_in_database'
    #     The entrypoint contain the three keys:
    #      -  user_data: dict,
    #      -  user_id: Optional[int] = None,
    #      -  user_email: Optional[str] = None.
    #
    #      Here is one option. It's when we have only the 'user_data'.
    #      '''json
    #      {
    #         "email": "premium25@example.com",
    #         "first_name": "testFirstName",
    #         "last_name": "testLastName",
    #         "password": "pbkdf2_sha256$hash_admin_1",
    #     }
    #     # or
    #     {
    #         "email": "premium25@example.com",
    #         "first_name": "testFirstName",
    #         "last_name": "testLastName",
    #         "password1": "pbkdf2_sha256$hash_admin_1",
    #         "password2": "pbkdf2_sha256$hash_admin_1",
    #     }
    #     '''
    #     It means by conditions, we should create a new user in database.
    #     In bode of method 'update_in_database' we have a check (self.is_email() method & 'test_is_email' test )"email" in db.
    #     If "email" email not exists in db. user will be created.
    #     PATH: persons.adapters.person_dabase_adapter.PersonServiceDatabaseAdapter.update_in_database
    #     :param mock_users_database: It is the mock-Users database model. All content of the mock database at the JSON-str
    #     :return: void
    #     """
    #
    #     from __tests__.fixtures.mock_function import get_file
    #     from persons.adapters import PersonServiceDatabaseAdapter
    #     mock_db_json_str: str = get_file()
    #
    #     new_user = {
    #         "email": "premium25@example.com",
    #         "first_name": "testFirstName",
    #         "last_name": "testLastName",
    #         "password1": "pbkdf2_sha256$hash_admin_1",
    #         "password2": "pbkdf2_sha256$hash_admin_1",
    #     }
    #     # --------------------
    #     person = PersonServiceDatabaseAdapter()
    #     result_email: bool = person.is_email("premium25@example.com")
    #
    #     assert result_email is not None
    #     assert result_email is False
    #
    #     # print("TEST DBUG BEFORE create person: " + str(person))
    #     mock_user_new:UsersPydantic =  person.update_in_database(new_user, mock_users_database["id"])
    #
    #     mock_user_new_json = json.loads(mock_user_new.model_dump_json())
    #     assert type(mock_user_new_json) == dict
    #
    #     mock_db_json_list: list[dict] = json.loads(mock_db_json_str)
    #     log.info(f"""\n
    #     # ============================================
    #     # TEST DEBUG THAT IS mock_db_json_list LENGTH (total moc database): {len(mock_db_json_list)}
    #     # THAT IS mock_db_json_list TYPE (total moc database): {type(mock_db_json_list)}
    #     # THAT IS mock_user_new_json (received a new single user) TYPE: {type(mock_user_new_json)}
    #     # THAT IS mock_user_new_json (received a new single user): {str(mock_user_new_json)}
    #     # ============================================
    #     """)
