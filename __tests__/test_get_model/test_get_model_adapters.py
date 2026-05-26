"""
PostmanAdapter.SubPerson
        ├── PersonBasisMixin (parent)
        └── CacherAdapterMixin (caching)

"""
import asyncio
import json
import logging
from asyncio import Lock

import pytest

from __tests__.fixtures.fixture_mock_patch import (
    mock_cacher_adapter_mixin,
    mock_mixin_method,
    mock_person_service_adapter,
    mock_pydantic_user,
    mock_subPerson_class,
    mock_user_django,
)

log = logging.getLogger(__name__)


class TestSubPostmanAdapter:

    @pytest.fixture
    def mock_test(self,mock_pydantic_user, mocker):
        from __tests__.fixtures.mock_function import (
            is_person_velidator,
        )

        return  mocker.Mock(side_effect=is_person_velidator(mock_pydantic_user))
    @pytest.mark.parametrize("person_em, person_id, expect", [
        (None, 1, True),
        ("test_2_mail@host.ru", None, True),
    ])
    async def test_subPerson_get_model(self, mock_cacher_adapter_mixin,mock_user_django, mock_subPerson_class,
                                       mock_test,mock_person_service_adapter,
                                       person_em, person_id,mock_mixin_method, expect) -> None:
        """
        Here chek the get_email conditions from the SubPerson.get_model of method.
        This is test 'persons.adapters.postman_adapter.PostmanAdapter.SubPerson.get_model' method.
        And addition. THe PostmanAdapter.SubPerson.__get_cache it is nock.
        :param mock_cacher_adapter_mixin: Fixture. This Mocks is the 'persons.adapters.cache_adapter.CacherAdapterMixin'  class
        :param mock_user_django: Fixture. This Mock-s  properties for the one person.
        :param mock_subPerson_class: Fixture. This Mock-s for the 'persons.adapters.postman_adapter.PostmanAdapter.SubPerson' subclass.
        :return: None or UsersPydantic/
        """
        log_t = f"[{self.__class__.__name__}][{self.test_subPerson_get_model.__name__}]: "
        from persons.adapters import PersonServiceAdapter, PostmanAdapter

        # database_service = PersonServiceAdapter()
        log.info(log_t + """\n
            # ============================================
            # Mock SubPerson
            # ============================================
            """)
        mock_subPerson = PostmanAdapter.SubPerson(person_email=person_em, person_index=person_id)
        mock_subPerson.database_service = mock_person_service_adapter
        mock_subPerson.log_t = "[Mock SubPerson]"
        log.info(f"""\n
            TEST DEBUG mock_user_django TYPE: {type(mock_user_django)} & EMAIL STR: {str(mock_user_django.__getattribute__("email"))} & ID STR: {str(mock_user_django.__getattribute__("id"))}
        """)
        mock_subPerson.person_index = mock_user_django.__getattribute__("id")
        mock_subPerson.person_email = mock_user_django.__getattribute__("email")

        log.info(log_t + """\n
        # ============================================
        # TEST test_get_new_model_data
        # ============================================
        """)
        lock = Lock()
        mock_subPerson_class.get_person_model = mock_mixin_method.get_person_model
        result_test: dict|None = await mock_subPerson.get_model(lock, mock_person_service_adapter)
        assert mock_subPerson_class.get_person_model is not None
        assert result_test is not None
        assert isinstance(result_test, dict)
        assert len(list(result_test.keys())) > 10
