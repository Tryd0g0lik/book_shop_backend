import logging

import pytest

from __tests__.fixtures.fixture_django2 import pytest_generate_tests
from persons.interfaces import (
    PersonServiceDatabaseAdapter as PersonServiceDatabaseAdapterInitialize,
)
from persons.models import Users
from utilities.adapters import PersonServiceDatabaseAdapter

# from unittest.mock import patch

# from django.db import models


log = logging.getLogger(__name__)


class TestCreateOrUpdateInDatabase:
    # fixtures = ["user_profiles.json"]
    PREFIX_LOG = "[TestCreateOrUpdateInDatabase]:"
    @pytest.fixture
    def fixture_create_user(self, new_users_registration):

        log_t = "{}[fixture_create_user]:".format(self.PREFIX_LOG[:-1])
        log.info("{} TEST FIXTURE # CREATE USER".format(log_t))
        log.info("{} TEST FIXTURE # EMAIL: {}".format(log_t, str(new_users_registration["email"])))

        new_users_registration: dict = new_users_registration
        del new_users_registration["check_user"]
        password: str = new_users_registration["password1"]
        del new_users_registration["password1"], new_users_registration["password2"]
        category: str  = new_users_registration["category"].strip()
        del new_users_registration["category"]
        passw_hash = PersonServiceDatabaseAdapter.hashes_password(password=password)

        new_users = new_users_registration.copy()
        new_users["password"] = passw_hash
        new_users_registration["password"] = password
        user = Users.objects.create(**new_users)
        user.groups.add(category)
        log.info("{} TEST FIXTURE # UPDATING DATA".format(log_t))
        log.info("{} TEST DEBUG EMAIL: {} ID: {}".format(log_t, str(user.email), str(user.id)))
        old_email: str = new_users_registration["email"]
        new_email: str = "new@email.com"

        log.info("{} TEST FIXTURE # CHANGING - EMAIL & PASSWORD".format(log_t))
        new_users_registration["email"] = new_email
        return [new_users_registration, user, old_email, new_email]

    # @pytest.fixture(scope="session", autouse=True)
    # def fixture_checker_model_userprofile(self, django_db_blocker):
    #     # from django.contrib.auth import get_user_model
    #     # from wagtail.users.models import UserProfile
    #     log_t = "{}[mocker_wagtail_model_userprofile]:".format(self.PREFIX_LOG[:-1])
    #     from django.apps import apps
    #     with django_db_blocker.unblock():
    #
    #         log.info("{} Before checking a model loading".format(log_t))
    #         try:
    #             user_profile_model = apps.get_model("wagtail.users.models", "UserProfile")
    #             log.info("{} ✅ The Model UserProfile loading.".format(log_t))
    #             for field in user_profile_model._meta.fields:
    #                 if field.is_relation:
    #                     log.info("{}    - {}: {}".format(self.PREFIX_LOG[:-1], field.name, field.verbose_name))
    #             # ----
    #             # yield user_profile_model
    #         except LookupError as e:
    #             #
    #             log.error("{} ❌ Model not found. Error = > {}".format(log_t, e.args[0] if e.args else str(e)))
    #             if not apps.is_installed("wagtail.users.models"):
    #                 log.warning("{} ❌ profiles app not installed.".format(log_t))
    #             # class UserProfile(models.Model):
    #             #     user = models.OneToOneField(Users, on_delete=models.CASCADE)
    #             # yield UserProfile
    #         except Exception as e:
    #             log.error("{} ❌ Error => {}".format(log_t, e.args[0] if e.args else str(e)))

                # if "App 'profiles' doesn't have" in str(e):
                #     class
                # Users = get_user_model()
                # person = Users.objects.all().first()
        #
        # with patch("wagtail.users.models.UserProfile") as mock:
        #     mock.user.return_value = person
        #     mock.user_id.return_value = person.id
        #     yield mock

    # @pytest.fixture
    # def mock_get_or_create_userprofile(self, mocker):
    #     from wagtail.users.models import UserProfile as WagtailUserProfile
    #     yield WagtailUserProfile


    @pytest.mark.django_db(transaction=True)
    def test_create_or_update_in_database_by_id(self,  fixture_create_user, mocker):
        """
        The purpose of test - This finding user by USER-INDEX and update the user data. Exclude is the property password.
        Testing the 'PersonServiceDatabaseAdapter.update_in_database'.
        :param fixture_create_user: It is "[< DICT_NEW_USER_DATA >, < USER_OBJECT_FROM_DB >, < OLD_USER_EMAIL >, < NEW_USER_EMAIL >]".
        :return: Assert what database will be containing two lines.
        """
        # create_or_update_in_database: PersonServiceDatabaseAdapterInitialize = (
        #     PersonServiceDatabaseAdapter.update_in_database
        # )
        log.info("DEBUG TEST 0")
        # MOcker
        # mock_celery_task_1 =  mocker.patch("persons.tasks.tasks_celery.task_set_cache.task_of_cache")
        # mock_celery_task_1.side_affect = lambda : True
        # mock_celery_task_2 =  mocker.patch("persons.tasks.tasks_celery.task_send_letter_to_user_email.task_postman")
        # mock_celery_task_2.side_effect = lambda : True
        #
        # # Mocker of Wagtail's Userprofile
        #
        # # UPDATE USER
        # log.info("DEBUG TEST 1")
        # new_users_data = fixture_create_user[0]
        # user = fixture_create_user[1]
        # new_email = fixture_create_user[-1]
        # user_dic = create_or_update_in_database(
        #     user_data=new_users_data, user_id=user.id
        # )
        # if user_dic is None:
        #     log.info(f"TEST DEBUG EMAIL: None")
        # else:
        #     log.info(f"TEST DEBUG EMAIL: {str(user_dic["email"])} ID: {user_dic["id"]}")
        # assert user_dic["email"] == new_email, "Response how a dictionary"
        #
        # user_filter = Users.objects.filter(email=new_email)
        # user_exists = user_filter.exists()
        # log.info(f"TEST DEBUG EXISTS: {str(user_exists)}")
        # assert user_exists, "User exists"
        # user = user_filter.first()
        # assert user.username not in user.password, "Password should not be changed"
        # assert user_dic["email"] == new_email, "Response how a dictionary"

    @pytest.mark.django_db()
    def test_create_or_update_in_database_by_email(self, fixture_create_user):
        """
        The purpose of this test - This finding user by EMAIL and update the user data. Exclude is the property password.
        Testing the 'PersonServiceDatabaseAdapter.update_in_database'.
        :param fixture_create_user: It is "[< DICT_NEW_USER_DATA >, < USER_OBJECT_FROM_DB >, < OLD_USER_EMAIL >, < NEW_USER_EMAIL >]".
        :return: Assert what database will be containing two lines.
        """
        # UPDATING USER
        create_or_update_in_database: PersonServiceDatabaseAdapterInitialize = (
            PersonServiceDatabaseAdapter.update_in_database
        )
        new_users_data = fixture_create_user[0]
        user = fixture_create_user[1]
        old_email = fixture_create_user[-2]
        new_email = fixture_create_user[-1]
        new_users_data["password"] = new_users_data["password"] + user.username
        user_dic = create_or_update_in_database(
            user_data=new_users_data, user_email=old_email
        )
        if user_dic is None:
            log.info(f"TEST DEBUG EMAIL: None")
        else:
            log.info(f"TEST DEBUG EMAIL: {str(user_dic["email"])} ID: {user_dic["id"]}")
        assert user_dic["email"] == new_email, "Response how a dictionary"
        user_filter = Users.objects.filter(email=new_email)
        assert user_filter.exists(), "User exists"
        user_first = user_filter.first()
        assert (
            user_first.username not in user_first.password
        ), "Password should not be changed"
        assert user_dic["email"] == new_email, "Response how a dictionary"

    @pytest.mark.django_db()
    def test_create_or_update_in_database_password(self, fixture_create_user):
        """
        The purpose of this test - This finding user by EMAIL and update the user data. Include is the property password.
        Testing the 'PersonServiceDatabaseAdapter.update_in_database'.
        :param fixture_create_user: It is "[< DICT_NEW_USER_DATA >, < USER_OBJECT_FROM_DB >, < OLD_USER_EMAIL >, < NEW_USER_EMAIL >]".
        :return: Assert what database will be containing two lines.
        """
        # UPDATING USER
        create_or_update_in_database: PersonServiceDatabaseAdapterInitialize = (
            PersonServiceDatabaseAdapter.update_in_database
        )
        new_users_data = fixture_create_user[0]
        user = fixture_create_user[1]
        old_email = fixture_create_user[-2]
        new_email = fixture_create_user[-1]
        log.info(f"TEST BEFORE UPDATE A PASSWORD")
        old_password = new_users_data["password"]
        new_password = new_users_data["password"] + user.username
        # ----
        new_users_data["old_password"] = old_password
        new_users_data["new_password"] = new_password
        del new_users_data["password"]

        user_dic = create_or_update_in_database(
            user_data=new_users_data, user_email=old_email
        )
        log.info(f"# CHECKING OF HASHING")
        assert user_dic["email"] == new_email, "Response how a dictionary"
        log.info("# BEFORE IT LEVEL - THE USER WAS UPDATED (in hashing")
        user_filter = Users.objects.filter(email=new_email)
        user_exists = user_filter.exists()
        user_first = user_filter.first()
        assert user_exists, "User exists"
        log.info("# HASHING OF PASSWORD")
        new_passw_hash = PersonServiceDatabaseAdapter.hashes_password(
            password=new_password
        )
        assert new_passw_hash == user_first.password, "Password was updated"
