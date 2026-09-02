# utilities/paginationcatalog.py:1
import logging
import math
from typing import (Any, Optional, TypeAlias, TYPE_CHECKING)
from catalog.apps import cachemanager_catalog
from project.settings_conf.settings_env import REST_FRAMEWORK_PAGINATION_SIZE

if TYPE_CHECKING:
    import queue
log = logging.getLogger(__name__)

C: TypeAlias = (list[dict[str, Any]] | str
            | dict[str, list[dict[str, Any]]] | str)

class PaginationCatalogData:
    PREFIX_LOG = "[PaginationCatalogData]"
    def __init__(
        self,
        page: Optional[int] = None,
        data_list: Optional[list[dict[str, Any]]] = None,
    ):
        f"""
        The {list[dict[str, Any]] | None} '__list' is data of type list[dict[str, Any]] that we want separate on chunks and
            that one chunk will send to the user.
        The {str | None} '__list_of_cache' is a JSON's string from the cache's server.
        The {str | None} '__key_cache' is a cache's key from the JSON's string.
        The {int| None} 'page' is a number of pages
        The {int| None } 'size_page' indicates the now much of lines can contain in one of chunk.
        The {int| None } '__user_index': The index of user which makes the unique cache key. 
        """
        self.__list: Optional[list[dict[str, Any]]] = data_list
        self.__list_of_cache: Optional[str[list[dict[str, Any]]]] = None
        self.__key_cache: Optional[str] = None
        self.page: Optional[int] = page
        self.size_page: Optional[int] = None
        self.count_page: Optional[int] = None
        self.__user_index: Optional[int] = None

    def __new__(cls, *args, **kwargs):
        """
        The 'size_page' it is value (by default) of size of count lines on the one page .
        """
        cls.size_page: int = REST_FRAMEWORK_PAGINATION_SIZE
        return super().__new__(*args, **kwargs)

    def get_chunk_data(self, chunk_size: int = 0, live_time = 60 * 7) -> list[dict[str, Any]]:
        """
        :param int chunk_size: It data that changing a default value from the 'self.size_page'
        :param int live_time: ( seconds ) it is a time of life the cache data/. Default value is 7 minutes.
        :return: The data it if all were successful or mistakes the 'ValueError' or 'Exception'.
        """
        # ============================================
        # GET PRIMARY DATA
        # ============================================
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.get_chunk_data.__name__)
        size_page = chunk_size if chunk_size > 0 else self.size_page
        chunk_queue: list[dict[str, Any]] = [] # The database's lines split on chunks
        dict_chunks: dict[str, Any] = dict() # Data for caching '{<page_number: < list_of_records_from_database>>}'
        try:
            # some code ....
            # ============================================
            # THE TOTAL LIST OF THE DATABASE DATA SEPARATE ON CHUNKS
            # ============================================
            # some code ....
            # ============================================
            # USE OF CACHE
            # ============================================
            # some code ....
        except ValueError as err:
            raise err
        except Exception as err:
            log_t = "{} Error => {}".format(prefix_log, err.args[0] if err.args else str(err))
            raise Exception(log_t) from err
        finally:
            # ============================================
            # CLEARING A SINGLE VARIABLE
            # ============================================
            self.get_cache_value = None

    def _record_cache(self, live_time: int = 60 * 7) -> bool:
        """
        :param int live_time: ( seconds ) it is a time of life the cache data/. Default value is 7 minutes.
        :return: The True it if all were successful cached or mistakes the 'ValueError' or 'Exception'.
        """
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self._record_cache.__name__)
        try:
            # some code ....
        except ValueError as err:
            raise err
        except Exception as err:
            log_t = "{} Error => {}".format(prefix_log, err.args[0] if err.args else str(err))
            raise Exception(log_t) from err
        return True


    def _get_cache(self,queue_collection: Optional[queue.Queue] = None,
                   collection: Optional[list | tuple] = None,
                   key_pattern: Optional[str] = None,
                   key: Optional[str] = None,
                   ex: Optional[int] = None,
                   px: Optional[int] = None,
                   exat: Optional[int] = None,
                   persist=None,) -> C:
        """
        You choose where could will saving the get's data. In the queue or the simple list.
        :param str key_pattern: This is the template of key. Default value is None. Example 'user:pending:*'
        :param str key: This is the one key.Key which get the data from the cache serve. Default value is None.
            Example: 'user:pending:< user email has hot containing '.' & '@' characters >'
        :param queue.Queue queue_collection: This is a queue for collecting data from the cache server. Default value is None.
        :param list|tuple collection: This is a list of tuple  for collecting  data from the cache server. Default value is None.
        :param int ex: (PX milliseconds ) This is a time of caching. That is the cache time of life. At getex
        :param int px: milliseconds  This is a time of caching. That is the cache time of life At getex
        :param exat: Timestamp=seconds. Set the specified Unix time in seconds, Default value is None
        :param persist: Remove the existing timeout on key, turning the key, Default value is None
        :return: None or mistakes the 'ValueError' or 'Exception'.
        """
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self._get_cache.__name__)
        try:
            cachemanager_catalog.get(
                queue_collection,
                collection,
                key_pattern,
                key,
                ex,
                px,
                exat,
                persist)
            if queue_collection is None and collection is None:
                log_t = "{} The cache data has been received not successfully.".format(prefix_log)
                raise ValueError(log_t)

            if collection is not None:
                self.get_cache_value =  collection

            self.get_cache_value = list(queue_collection.queue)
        except Exception as err:
            log_t = "{} Error => {}".format(prefix_log, err.args[0] if err.args else str(err))
            raise Exception(log_t) from err

    @property
    def get_cache_value(self) -> C:
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.get_cache_value.__name__)
        if self.__list_of_cache is None:
            log_t = "{} No data received".format(prefix_log)
            raise ValueError(log_t)
        return self.__list_of_cache

    @get_cache_value.setter
    def get_cache_value(self, value: C) -> None:
        self.__list_of_cache = value

    @property
    def get_cache_key(self) -> str:
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.get_cache_key.__name__)
        if self.__key_cache is None:
            log_t = "{} No data received".format(prefix_log)
            raise ValueError(log_t)
        return self.__key_cache

    @get_cache_key.setter
    def get_cache_key(self, key: str) -> None:
        self.__key_cache = key

    @property
    def get_list(self) -> list[dict[str, Any]]:
        """FOre get and return data for pagination."""
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.get_list.__name__)
        if self.__list is None:
            log_t = "{} No data received".format(prefix_log)
            raise ValueError(log_t)
        return self.__list

    @get_list.setter
    def get_list(self, data: list[dict[str, Any]]) -> None:
        self.__list = data

    @property
    def get_user_index(self) -> int:
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.get_user_index.__name__)
        if self.__user_index is None:
            log_t = "{} No data received".format(prefix_log)
            raise ValueError(log_t)
        return self.__user_index

    @get_user_index.setter
    def get_user_index(self, index: int) -> None:
        self.__user_index = index
