# __tests__/tests_services/test_user_service_adapter.py:1
import json
import logging
from unittest.mock import MagicMock

import pytest

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import (
    mock_database_get_user_model,
    mock_users_database,
)
from __tests__.fixtures.mock_function import get_file
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

    def test_create_user(self, mocker, mock_users_database ):
        from __tests__.fixtures.mock_function import get_one_user, save_one_user
        from persons.adapters import PersonServiceAdapter
        from persons.models import Users

        # -------------------- MockDatabaseServiceFile
        # mock_db = MockDatabaseServiceFile()
        # mock_db.is_file()
        # file_of_db = mock_db.get_file()
        # file_of_db = get_file()
        #
        # file_of_db = json.loads(file_of_db)
        # assert isinstance(file_of_db, list)
        # assert type(file_of_db[0]) is dict
        # def side_affect_fun(**kwargs):
        #     email = kwargs.get("email")
        #     print(f"TEST DEBUG side_affect_fun: {str(email)}")
        #     return get_one_user(email, database=file_of_db)
        # # -------------------- Users()
        # # mock_users_class = MagicMock(name=Users)
        # mock_method_Users = mocker.patch("persons.models.Users")
        #
        # mock_method_get = mock_method_Users.objects.get
        # mock_method_get.side_effect = side_affect_fun
        #
        # # mock_method_create = mocker.patch("persons.models.models_persons.Users")
        # mock_method_create = mock_method_Users.objects.create
        # mock_method_create.side_effect = \
        #     lambda **kwargs: save_one_user(file_of_db, **kwargs)
        # --------------------
        person = PersonServiceAdapter()
        result_email: bool = person.is_email("premium25@example.com")

        assert result_email is not None
        assert result_email is False

        # print("TEST DBUG BEFORE create person: " + str(person))
        # result:UsersPydantic =  person.create_or_update_in_database(user_data={
        #     "email": "premium25@example.com",
        #     "first_name": "testFirstName",
        #     "last_name": "testLastName",
        #     "password": "pbkdf2_sha256$hash_admin_1",
        # })
        # # result_json = json.loads(result.model_dump_json())
        # assert type(result) == dict
        # mock_users_class.reset_mock()
        # ------------------------
        # u = user_new.get()
        #
        # assert type(user_new) is dict
        # del user_new["id"], user_new["is_superuser"], user_new["email"],  user_new["is_staff"], user_new["is_active"]
        # del user_new["is_sent"], user_new["is_verified"], user_new["verification_code"], user_new["balance"]
        # del user_new["created_at"], user_new["updated_at"], user_new["last_login"], user_new["date_joined"]

        # person_service_adapter.create_or_update_in_database()
        # mcok_file_db.close_file()
