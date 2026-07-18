# __tests__/tests_database/tests_create_or_update_in_database.py:1
# Here use successful data.
import logging

import pytest
from django.contrib.auth.models import Group

from __tests__.fixtures.fixture_django2 import pytest_generate_tests
from persons.interfaces import (
    PersonServiceDatabaseAdapter as PersonServiceDatabaseAdapterInitialize,
)
from persons.models import Users
from utilities import CATEGORY_STATUS
from utilities.adapters import PersonServiceDatabaseAdapter

log = logging.getLogger(__name__)


class TestCreateOrUpdateInDatabase:

    PREFIX_LOG = "[TestCreateOrUpdateInDatabase]:"
    @pytest.fixture()
    def fixture_create_user(self,transactional_db, new_users_registration):
        log_t = "{}[fixture_create_user]:".format(self.PREFIX_LOG[:-1])
        log.info("{} TEST FIXTURE # EMAIL: {}".format(log_t, str(new_users_registration["email"])))
        # ============================================
        # CREATING COLLECTION OF CROUPS NAMES
        # ============================================
        for item in CATEGORY_STATUS:
            if Group.objects.filter(name=item[1]).count() == 0:
                Group.objects.create(name=item[1])
                log.info("{} Group {} created!".format(log_t, item[1]))
                Group.objects.get(name=item[1])
                log.info("{} Group {} checked in database!".format(log_t, item[1]))
        # ============================================
        # GETTING DATA OF TEST
        # ============================================
        new_users_registration: dict = new_users_registration
        del new_users_registration["check_user"]
        # --- category
        category: str = new_users_registration["category"].strip()
        del new_users_registration["category"]
        # --- passwords
        password: str = new_users_registration["password1"]
        del new_users_registration["password1"], new_users_registration["password2"]
        passw_hash = PersonServiceDatabaseAdapter.hashes_password(password=password)

        new_users = new_users_registration.copy()
        new_users["password"] = passw_hash
        new_users_registration["password"] = password

        # --- email
        old_email: str = new_users_registration["email"]
        new_email: str = "new@email.com"
        log.info("{} TEST FIXTURE # CHANGING - EMAIL & PASSWORD".format(log_t))
        new_users_registration["email"] = new_email
        # ============================================
        # CREATING OF USER
        # ============================================
        user = Users.objects.create(**new_users)
        category_queryset = Group.objects.filter(name=category.capitalize())
        try:
            category_obj = category_queryset.first()
            user.groups.add(category_obj)
        except (InterruptedError, LookupError) as e:
            log.error("{} TEST ERROR => {}".format(log_t, e.args[0] if e.args else str(e)))
            raise e
        return [new_users_registration, user, old_email, new_email]

    @pytest.mark.django_db(transaction=True)
    def test_create_or_update_in_database_by_id(self, transactional_db, fixture_create_user, mocker):
        """
        The purpose of test - This finding user by USER-INDEX and update the user data. Exclude is the property password.
        Testing the 'PersonServiceDatabaseAdapter.update_in_database'.
        :param fixture_create_user: It is "[< DICT_NEW_USER_DATA >, < USER_OBJECT_FROM_DB >, < OLD_USER_EMAIL >, < NEW_USER_EMAIL >]".
        :return: Assert what database will be containing two lines.
        """
        log_t = "{}[test_create_or_update_in_database_by_id]:".format(self.PREFIX_LOG[:-1])
        create_or_update_in_database: PersonServiceDatabaseAdapterInitialize = (
            PersonServiceDatabaseAdapter.update_in_database
        )
        # ============================================
        # UPDATE USER's DATA
        # ============================================
        new_users_data = fixture_create_user[0]
        user = fixture_create_user[1]
        new_email = fixture_create_user[-1]
        user_dic = create_or_update_in_database(
            user_data=new_users_data, user_id=user.id
        )
        if user_dic is None:
            log.info("{} TEST DEBUG EMAIL: None".format(log_t))
        else:
            log.info("{} TEST DEBUG EMAIL: {} ID: {}".format(log_t,str(user_dic["email"]), user_dic["id"]))
        assert user_dic["email"] == new_email, "Response how a dictionary"
        # ============================================
        # HERE IS CHECKING DATA OF DATABASE THEY UPDATING OR NOT
        # ============================================
        user_filter = Users.objects.filter(email=new_email)
        user_exists = user_filter.exists()
        log.info("{} TEST DEBUG EXISTS: {}".format(log_t, str(user_exists)))
        assert user_exists, "User exists"
        user = user_filter.first()
        assert user.username not in user.password, "Password should not be changed"
        assert user_dic["email"] == new_email, "Response how a dictionary"
        log.info("{} TEST SUCCESSFUL ✅".format(log_t))

    @pytest.mark.django_db()
    def test_create_or_update_in_database_by_email(self, fixture_create_user):
        """
        The purpose of this test - This finding user by EMAIL and update the user data. Exclude is the property password.
        Testing the 'PersonServiceDatabaseAdapter.update_in_database'.
        :param fixture_create_user: It is "[< DICT_NEW_USER_DATA >, < USER_OBJECT_FROM_DB >, < OLD_USER_EMAIL >, < NEW_USER_EMAIL >]".
        :return: Assert what database will be containing two lines.
        """
        log_t = "{}[test_create_or_update_in_database_by_email]:".format(self.PREFIX_LOG[:-1])
        # ============================================
        # UPDATE USER's DATA
        # ==============================================
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
            log.info("{} TEST DEBUG EMAIL: None".format(log_t))
        else:
            log.info("{} TEST DEBUG EMAIL: {} ID: {}".format(log_t, str(user_dic["email"]), user_dic["id"]))
        # ============================================
        # HERE IS CHECKING DATA OF DATABASE THEY UPDATING OR NOT
        # ============================================
        assert user_dic["email"] == new_email, "Response how a dictionary"
        user_filter = Users.objects.filter(email=new_email)
        assert user_filter.exists(), "User exists"
        user_first = user_filter.first()
        assert (
            user_first.username not in user_first.password
        ), "Password should not be changed"
        assert user_dic["email"] == new_email, "Response how a dictionary"
        log.info("{} TEST SUCCESSFUL ✅".format(log_t))

    @pytest.mark.skip(reason="CHeck method 'update_in_database'. Passwords are difference on the complete")
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
