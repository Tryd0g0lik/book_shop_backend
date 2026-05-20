# __tests__/fixtures/fixture_mock_patch.py:1
import logging

import pytest

from __tests__.fixtures.fixture_django import mock_user_django
from __tests__.fixtures.fixture_pydantic import mock_pydantic_user

log = logging.getLogger(__name__)




@pytest.fixture
def mock_mixin_method(mock_pydantic_user, mock_user_django, mocker):
    log.info("""\n
    # ============================================
    # FIXTURE PersonBasisMixin
    # ============================================
    """)
    mock_mixin_class =  mocker.patch("persons.adapters.person_base.PersonBasisMixin"
                             )
    mock_personBasisMixin = mock_mixin_class.return_value
    mock_personBasisMixin.log_t = "[Mock PersonBasisMixin]"
    mock_personBasisMixin.person_index = None
    mock_personBasisMixin.person_email = mock_user_django.__getattribute__("email")  # "test_2_mail@host.ru"
    mock_personBasisMixin.get_email = mocker.Mock(return_value=mock_user_django.__getattribute__("email"))
    mock_personBasisMixin.get_person_model = mocker.MagicMock(return_value=None)
    yield mock_mixin_class

@pytest.fixture
def mock_cacher_adapter_mixin(mocker):
    log.info("""
    # ============================================
    # FIXTURE CacherAdapterMixin
    # ============================================
    """)
    mock_mixin_class = mocker.patch("persons.adapters.cache_adapter.CacherAdapterMixin")
    mock_cacherAdapterMixin = mock_mixin_class.return_value
    mock_cacherAdapterMixin.log_t = "[Mock CacherAdapterMixin]:"
    mock_cacherAdapterMixin._pool = None
    mock_cacherAdapterMixin.__pool_lock = None
    mock_cacherAdapterMixin._init_pool = mocker.Mock(return_value=None)
    mock_cacherAdapterMixin.get_person_model = mocker.Mock(return_value=None)
    return mock_mixin_class

@pytest.fixture
def mock_person_service_adapter(mock_pydantic_user,  mocker):
    log.info("""\n
    # ============================================
    # FIXTURE PersonServiceAdapter
    # ============================================
    """)
    mock_adapter_class = mocker.patch("persons.adapters.person_service_adapter.PersonServiceAdapter")
    mock_adapter_class.get_user_by_id = mocker.Mock(return_value=mock_pydantic_user)
    def database_service_get_user_by_email(user_email=None):

        return mock_pydantic_user

    mock_adapter_class.get_user_by_email = mocker.Mock(side_effect=database_service_get_user_by_email)
    mock_adapter_class.search_by_email = mocker.Mock(return_value=[mock_pydantic_user])

    yield mock_adapter_class

@pytest.fixture
def mock_subPerson_class(mock_mixin_method, mock_person_service_adapter,
                         mock_user_django, mock_pydantic_user, mocker):
    from persons.adapters import PostmanAdapter
    log.info("""
    # ============================================
    # FIXTURE SubPerson
    # ============================================
    """)
    email = mock_user_django.__getattribute__("email")
    mock_subPerson = PostmanAdapter.SubPerson(person_email=email)
    log.info("""
    # ============================================
    # SubPerson
    # ============================================
    """)
    mock_subPerson.__init__ = mocker.Mock(return_value=None)
    mock_subPerson.database_service = mock_person_service_adapter
    mock_subPerson.log_t = "[Mock SubPerson]"
    mock_subPerson.person_index = None
    mock_subPerson.person_email = mock_user_django.__getattribute__("email") # "test_2_mail@host.ru"

    def is_person_velidator(value=None):
        if mock_pydantic_user is None:
            raise TypeError(f"Expected UsersPydantic, got {type(mock_pydantic_user)}")
        return True

    mock_subPerson._is_person = mocker.Mock(side_effect=is_person_velidator)
    mock_subPerson._get_data = mocker.Mock(return_value=mock_pydantic_user)

    return  mock_subPerson
