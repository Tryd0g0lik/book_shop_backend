# __tests__/fixtures/fixture_mock_patch.py:1
import json
import logging
from unittest.mock import MagicMock, Mock

import pytest

from __tests__.fixtures.fixture_django import (
    generate_users,
    mock_user_django,
    pytest_generate_tests,
)
from __tests__.fixtures.fixture_pydantic import mock_pydantic_user
from __tests__.fixtures.mock_function import get_file, save_one_user
from persons.adapters import PersonServiceDatabaseAdapter
from persons.interfaces import UsersPydantic

log = logging.getLogger(__name__)

log.info("""
# ============================================
# __tests__/fixtures/fixture_mock_patch.py:1
# ============================================
""")


@pytest.fixture
def mock_mixin_method(mock_pydantic_user, mock_user_django, mocker):
    log.info("""\n
    # ============================================
    # FIXTURE PersonBasisMixin
    # ============================================
    """)
    mock_mixin_class =  mocker.patch("persons.adapters.person_base.PersonBasisMixin")
    mock_personBasisMixin = mock_mixin_class.return_value
    mock_personBasisMixin.log_t = "[Mock PersonBasisMixin]"
    mock_personBasisMixin.person_index = None
    mock_personBasisMixin.person_email = mock_user_django.__getattribute__("email")  # "test_2_mail@host.ru"
    mock_personBasisMixin.get_email = MagicMock(return_value=mock_user_django.__getattribute__("email"))
    mock_personBasisMixin.get_person_model = MagicMock(return_value=mock_user_django)
    yield mock_mixin_class

@pytest.fixture
def mock_cacher_adapter_mixin(mocker):
    log.info("""
    # ============================================
    # FIXTURE CacherAdapter
    # ============================================
    """)
    mock_mixin_class = mocker.patch("persons.adapters.cache_adapter.CacherAdapter")
    mock_cacherAdapterMixin = mock_mixin_class.return_value
    mock_cacherAdapterMixin.log_t = "[Mock CacherAdapter]:"
    mock_cacherAdapterMixin._pool = None
    mock_cacherAdapterMixin._pool_lock = None
    mock_cacherAdapterMixin._init_pool = mocker.Mock(return_value=None)
    mock_cacherAdapterMixin.get_person_model = mocker.Mock(return_value=None)
    return mock_mixin_class

@pytest.fixture
def mock_person_service_adapter(mock_pydantic_user,  mocker):
    from __tests__.fixtures.mock_function import (
        database_service_get_user_by_email,
        database_service_get_user_by_id,
    )
    log.info("""\n
    # ============================================
    # FIXTURE PersonServiceAdapter
    # ============================================
    """)
    mock_adapter_class = mocker.patch("persons.adapters.person_database_adapter.PersonServiceDatabaseAdapter")
    mock_adapter_class.get_user_by_id.return_value = database_service_get_user_by_id(mock_pydantic_user)
    mock_adapter_class.get_user_by_email.return_value = database_service_get_user_by_email(mock_pydantic_user)
    mock_adapter_class.search_by_email = mocker.Mock(return_value=[mock_pydantic_user])

    yield mock_adapter_class

@pytest.fixture
def mock_subPerson_class(mock_pydantic_user, mocker):
    from persons.adapters import PostmanAdapter
    log.info("""
    # ============================================
    # FIXTURE SubPerson
    # ============================================
    """)
    mock_postman = mocker.patch("persons.adapters.postman_adapter.PostmanAdapter")
    mock_sub_person = mocker.patch.object(PostmanAdapter.SubPerson, "_get_data", )
    mock_sub_person.return_value = [json.loads(mock_pydantic_user.model_dump_json())]
    mock_postman.SubPerson._get_data = mock_sub_person
    return  mock_postman

@pytest.fixture
def mock_database_get_user_model_2(mocker,users_model_data):
    log.info("""\n
    # ============================================
    # FIXTURE BEFORE BEFORE CREATE THE MOCK FOR THEM:
    # - persons.models.Users
    # - persons.models.Users.objects.get
    # ============================================
    """)
    mock_users = mocker.patch("persons.models.Users")
    log.info(f"""\n
    # ============================================
    #  TESST DEBUG users_model_data: {str(users_model_data)}
    # ============================================
    """)
    mockUsersObject = UsersPydantic(**users_model_data)

    mock_users_object_get = mock_users.objects.get
    mock_users_object_get.return_value = mockUsersObject
    yield mock_users
    log.info(f"\n\tTEST DEBUG call_args args: {mock_users_object_get.call_args}")
    log.info(f"TEST DEBUG call_args_list: {mock_users_object_get.call_args_list}")

@pytest.fixture
def mock_database_get_user_model(mocker, users_model_data):
    """
    TODO: Пересмотреть логику.
    Пересмотреть
    :param mocker:
    :param users_model_data:
    :return:
    """
    from django.core.mail import send_mail

    from persons.models import Users

    log.info("""
    # ============================================
    # CREATE Object of the Users model
    # ============================================
    """)
    MockUserClass = Mock(spec=[
        'id', 'username', 'email', 'password', 'first_name', 'last_name',
        'last_login', 'is_active', 'is_staff', 'is_superuser', 'is_sent',
        'is_verified', 'category', 'balance', 'verification_code',
        'created_at', 'updated_at', 'date_joined'
    ])
    MockUserClass.email_user = lambda subject, message, recipient_list, from_email=None, **kwargs: send_mail(subject, message, recipient_list, from_email, **kwargs)
    mock_user = MockUserClass()
    mock_user.configure_mock(**users_model_data)
    mock_users_model = mocker.patch.object(Users.objects, "get",return_value=mock_user )
    mock_users_model.object.get.return_value = mock_user
    mocker.patch("persons.models.Users")
    yield mock_user

# ============================================
# MOCK DATABASE Users TO THE TestUserServiceAdapter TEST
# ============================================
@pytest.fixture
def mock_users_database(mocker):
    from __tests__.fixtures.mock_function import get_one_user


    log.info("""\n
    # ============================================
    # FIXTURE BEFORE GETS A MOCK USER OF DATABASE
    # ============================================
    """)
    file_of_db = get_file()

    file_of_db = json.loads(file_of_db)
    assert isinstance(file_of_db, list)
    assert type(file_of_db[0]) is dict
    log.info("""\n
    # ============================================
    # FIXTURE BEFORE GETS A MOCK LOGIC FOR THE Django's Users.objects.get
    # ============================================
    """)
    def side_affect_fun(**kwargs):
        email = kwargs.get("email")
        print(f"TEST DEBUG side_affect_fun: {str(email)}")
        return get_one_user(email, database=file_of_db)

    log.info("""\n
    # ============================================
    # FIXTURE BEFORE BEFORE CREATE THE MOCK FOR THEM:
    # - persons.models.Users
    # - persons.models.Users.objects.get
    # - persons.models.Users.objects.create
    # ============================================
    """)
    mock_method_Users = mocker.patch("persons.models.Users")
    mock_method_Users.reset_mock()
    mock_method_get = mock_method_Users.objects.get
    mock_method_get.side_effect = side_affect_fun

    mock_method_create = mock_method_Users.objects.create
    mock_method_create.side_effect = \
        lambda **kwargs: save_one_user(file_of_db, **kwargs)

    yield mock_method_Users

    log.info("""\n
    # ============================================
    # FIXTURE COMPLETING THE TEST AND THIS IS BEFORE THE MOCK REPORT
    # ============================================
    """)
    log.info(f"\tTEST DEBUG call_args args: {mock_method_get.call_args.args}")
    log.info(f"TEST DEBUG call_args kwargs: {mock_method_get.call_args.kwargs}")
    log.info(f"TEST DEBUG call_args_list: {mock_method_get.call_args_list}")
    log.info(f"TEST DEBUG method_calls: {mock_method_get.method_calls}")
