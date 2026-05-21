"""
PostmanAdapter.SubPerson
        ├── PersonBasisMixin (parent)
        ├── PersonServiceAdapter (database_service)
        └── CacherAdapterMixin (caching)

"""

import logging

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



    async def test_subPerson_get_model(self, mock_cacher_adapter_mixin,mock_user_django, mock_subPerson_class) -> None:
        """
        This is test 'persons.adapters.postman_adapter.PostmanAdapter.SubPerson.get_model' method
        :param mock_cacher_adapter_mixin: Fixture. This Mocks is the 'persons.adapters.cache_adapter.CacherAdapterMixin'  class
        :param mock_user_django: Fixture. This Mock-s  properties for the one person.
        :param mock_subPerson_class: Fixture. This Mock-s for the 'persons.adapters.postman_adapter.PostmanAdapter.SubPerson' subclass.
        :return: None or UsersPydantic/
        """
        from asyncio import Lock
        log.info("""\n
        # ============================================
        # TEST test_get_new_model_data
        # ============================================
        """)
        lock = Lock()
        mock_subPerson_class.get_person_model = None
        result_test = await mock_subPerson_class.get_model(lock)
        log.info(f"[test_get_new_model_data]: TEST DEBUG RESULT: {str(result_test)} TYPE: {type(result_test)}")
        assert result_test is not None
