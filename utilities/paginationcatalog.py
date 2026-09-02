# utilities/paginationcatalog.py:1
import logging
from typing import Any, Optional

from project.settings_conf.settings_env import REST_FRAMEWORK_PAGINATION_SIZE
log = logging.getLogger(__name__)

class PaginationCatalogData:
    PREFIX_LOG = "[PaginationCatalogData]"
    def __init__(
        self,
        data_list: Optional[list[dict[str, Any]]] = None,
    ):
        f"""
        The {list[dict[str, Any]] | None} '__list' is data of type list[dict[str, Any]] that we want separate on chunks and
            that one chunk will send to the user.
        The {str[list[dict[str, Any]]] | None} '__list_of_cache' is a JSON's string from the cache's server.
        The {str | None} '__key_cache' is a cache's key from the JSON's string.
        The {int| None} 'page' is a number of pages
        The {int| None } 'size_page' indicates the now much of lines can contain in one of chunk. 
        """
        self.__list: Optional[list[dict[str, Any]]] = data_list
        self.__list_of_cache: Optional[str[list[dict[str, Any]]]] = None
        self.__key_cache: Optional[str] = None
        self.page: Optional[int] = None
        self.size_page: Optional[int] = None
    def __new__(cls, *args, **kwargs):
        """
        The 'size_page' it is value (by default) of size of count lines on the one page .
        """
        cls.size_page: int = REST_FRAMEWORK_PAGINATION_SIZE
        return super().__new__(*args, **kwargs)
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

    def get_chunk_data(self, chunk_size: int = 0) -> list[dict[str, Any]]:
        """
        :param int chunk_size: It data that changing a default value from the 'self.size_page'
        :return:
        """
        prefix_log = "{}[{}]:".format(self.PREFIX_LOG, self.get_chunk_data.__name__)
        size_page = chunk_size if chunk_size > 0 else self.size_page
        try:
            data_list: list[dict[str, Any]] = self.get_list
            # ============================================
            # The logic of pagination and caching for working in the catalog code
            # ============================================

        except ValueError as err:
            raise err
        except Exception as err:
            log_t = "{} Error => {}".format(prefix_log, err.args[0] if err.args else str(err))
            raise Exception(log_t) from err
