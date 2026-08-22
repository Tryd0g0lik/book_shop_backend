# __tests__/tests_api/fixture_creater_users.py:1
import logging

import pytest
from django.db.models import QuerySet

# THE LINE BELOW/under it ( this notification) NOT DELETE!!
# from __tests__.fixtures.fixture_parametrize2 import pytest_generate_tests

log = logging.getLogger(__name__)


@pytest.fixture
def fixture_create_user( db, new_users_registration):
    """here is we creating a User (From common usr's data) in database and
     transmit the user data to the next test method. """
    prefix_log: str = ""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    from django.core.management import call_command
    log_t = "{}[fixture_create_user]:".format(prefix_log, )
    # ============================================
    # Create a test's environment
    # ============================================
    # call_command("user_groups_db")
    call_command("permissions")
    log.info("{} Fulling the name of groups/roles in database.".format(log_t))
    Users = get_user_model()

    # ============================================
    # FILLING USER DATA TO THE DATABASE
    # ============================================
    password: str = new_users_registration["password1"]
    category: str = new_users_registration["category"]
    del new_users_registration["password1"], new_users_registration["password2"], \
        new_users_registration["check_user"], new_users_registration["category"]
    new_users_registration["password"] = password
    user, _ = Users.objects.get_or_create(**new_users_registration)
    # --- user group/role/permissions
    # ============================================
    # ADD A USER's GROUP
    #  it is regulator of permissions/right
    # ============================================
    group_name = category.capitalize()
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    if created:
        log.info("{} Group '{}' created successfully!".format(log_t, group_name))
    else:
        log.info("{} Group {} already exists!".format(log_t, group_name))
    role_queryset: QuerySet = user.groups.values_list("name", flat=True)
    assert role_queryset.count() == 1
    log.info(
        "{} Created user. User Index: {} email: {} role: {}".format(log_t, user.id, new_users_registration["email"],
                                                                    role_queryset.first()))
    log.info("{} User got a group {}.".format(log_t, (user.groups.first()).name))
    yield user
