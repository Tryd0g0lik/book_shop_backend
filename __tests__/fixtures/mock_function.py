# __tests__/fixtures/mock_function.py:1
import logging
from typing import Optional

log = logging.getLogger(__name__)


# ============================================
# MOCK SUB PERSON CLASS
# ============================================
def __get_cache_staticmethod(value: str = None):
    from persons.services import CacheManager
    log.info("""
            # ============================================
            # Mock __get_cache_staticmethod vs SubPerson.__get_cache
            # ============================================
            """)
    cachemanager_test = CacheManager()
    # value_of_cache: Optional[bytes] = None
    value_of_cache: Optional[list | dict] = []
    log.info(f"[Mock __get_cache.CacheManager ]: Before Value: {str(value)}")
    cachemanager_test.get(key=value, collection=value_of_cache, exat=86400)

    log.info(f"[Mock __get_cache.CacheManager ]: After result {str(value_of_cache)}")
    return value_of_cache


def is_person_velidator(mock_pydantic_user):
    def wrapper(value=None):

        log.info(
            """
            # ============================================
            # Mock is_person_velidator vs SubPerson._is_person
            # ============================================
            """)
        if mock_pydantic_user is None:
            raise TypeError(f"Expected UsersPydantic, got {type(mock_pydantic_user)}")
        return True
    return wrapper

# ============================================
# MOCK PERSON SERVICE ADAPTER
# ============================================
def database_service_get_user_by_email(mock_pydantic_user):
    def wrapper(user_email=None):
        log.info(
            """
            # ============================================
            # Mock database_service_get_user_by_email vs PersonServiceAdapter.get_user_by_emai
            # ============================================
            """)
        return mock_pydantic_user
    return wrapper
