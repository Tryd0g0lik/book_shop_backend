"""
PostmanAdapter.SubPerson
        ├── PersonBasisMixin (parent)
        ├── PersonServiceAdapter (database_service)
        └── CacherAdapterMixin (caching)

"""

import logging

import pytest

from __tests__.fixtures.fixture_django import mock_pydantic_user, mock_user_django

log = logging.getLogger(__name__)

class TestSubPostmanAdapter:

    @pytest.fixture
    def mock_mixin_method(self,mock_pydantic_user, mocker):
        log.info("""\n
        # ============================================
        # FIXTURE PersonBasisMixin
        # ============================================
        """)
        mock_mixin_class =  mocker.patch("persons.adapters.person_base.PersonBasisMixin"
                                 )
        mock_personBasisMixin = mock_mixin_class.return_value
        # mock_personBasisMixin.__init__ = mocker.Mock(return_value={"log_t": "[Mock PersonBasisMixin]"})
        mock_personBasisMixin.log_t = "[Mock PersonBasisMixin]"
        mock_personBasisMixin.person_index = None
        mock_personBasisMixin.person_email = "test_2_mail@host.ru"
        mock_personBasisMixin.get_email = mocker.Mock(return_value="test_2_mail@host.ru")
        mock_personBasisMixin.get_person_model = mocker.MagicMock(return_value=None)



        yield mock_mixin_class

    @pytest.fixture
    def mock_cacher_adapter_mixin(self, mocker):
        log.info("""\n
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
    def mock_person_service_adapter(self,mock_pydantic_user,  mocker):
        log.info("""\n
        # ============================================
        # FIXTURE PersonServiceAdapter
        # ============================================
        """)
        mock_adapter_class = mocker.patch("persons.adapters.person_service_adapter.PersonServiceAdapter")
        mock_adapter_class.get_user_by_id = mocker.Mock(return_value=mock_pydantic_user)
        def database_service_get_user_by_email(user_email="test_2_mail@host.ru"):

            return mock_pydantic_user

        mock_adapter_class.get_user_by_email = mocker.MagicMock(side_effect=database_service_get_user_by_email)
        mock_adapter_class.search_by_email = mocker.Mock(return_value=[mock_pydantic_user])

        yield mock_adapter_class

    @pytest.fixture
    def mock_subPerson_class(self, mock_mixin_method, mock_person_service_adapter, mock_pydantic_user, mocker):
        from persons.adapters import PostmanAdapter
        log.info("""\n
        # ============================================
        # FIXTURE SubPerson
        # ============================================
        """)
        mock_subPerson = PostmanAdapter.SubPerson(person_email="test_2_mail@host.ru")
        # mock_postmanAdapter = mocker.patch("persons.adapters.PostmanAdapter.SubPerson")
        log.info("""
        # ============================================
        # SubPerson
        # ============================================
        """)
        # mock_subPerson = mock_postmanAdapter.return_value
        mock_subPerson.__init__ = mocker.Mock(return_value=None)
        mock_subPerson.database_service = mock_person_service_adapter
        mock_subPerson.log_t = "[Mock SubPerson]"
        mock_subPerson.person_index = None
        mock_subPerson.person_email = "test_2_mail@host.ru"

        def is_person_velidator(value=None):
            if mock_pydantic_user is None:
                raise TypeError(f"Expected UsersPydantic, got {type(mock_pydantic_user)}")
            return True

        mock_subPerson._is_person = mocker.Mock(side_effect=is_person_velidator)
        mock_subPerson._get_data = mocker.Mock(return_value=mock_pydantic_user)

        return  mock_subPerson




    async def test_subPerson_get_model(self, mock_cacher_adapter_mixin, mock_subPerson_class):
        from asyncio import Lock
        log.info("""\n
        # ============================================
        # TEST test_get_new_model_data
        # ============================================
        """)
        lock = Lock()
        mock_subPerson_class.get_person_model = None
        result_test = await mock_subPerson_class.get_model(lock)
        log.info(f"[test_get_new_model_data]: RESULT TEST: {str(result_test)} TYPE: {type(result_test)}")
        assert result_test is not None
