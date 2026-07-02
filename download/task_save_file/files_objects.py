# download/task_save_file/files_objects.py:1
import logging
import os
import re

from project import settings

log = logging.getLogger(__name__)
PATH_ERROR_DIR = os.path.join(settings.MEDIA_ROOT, "error_catalog")
TEMPLATE_NAME_OF_FILES = r"(^product_error_[0-9-_]+\.txt)$"

MAX_FILE_SIZE = 200 * 1024


# ============================================
# FILE OBJECT
# ============================================
class Files:
    def __init__(self, path: str):
        self.path = path
        self._get_directory_exists()

    def get_list_files(self):
        listdir = os.listdir(self.path)
        try:
            return [item for item in listdir if re.search(TEMPLATE_NAME_OF_FILES, item)]
        except FileNotFoundError:
            return []

    def _get_directory_exists(self) -> None:
        try:
            os.makedirs(PATH_ERROR_DIR, exist_ok=True)
            log.info(
                "[get_directory_exists]: Directory exists for collection of lost data"
            )
        except FileExistsError:
            log.warning("[get_directory_exists]: Something what wrong.")

    def get_empty_file(self) -> str | None:
        """
        Get an empty file by path it is self.path (:var path_error_dir) and
         a template of the file name 'product_error_%d-%m-%Y_%H-%M-%S.txt'.
        It is getting a full list of file's names.
        Then do checking the size of the file.  If size < MAX_FILE_SIZE mean return the name file
        else return None
        :return: str | None
        """
        list_str: list = self.get_list_files()
        for name in list_str:
            if self.is_file(name):
                full_path = os.path.join(self.path, name)
                if os.path.getsize(full_path) < MAX_FILE_SIZE:
                    return name
        return None

    def is_file(self, name: str) -> bool:
        """
        Check if a file exists.
        :param name: This is a file name.
        :return: Ture if file exists or False if not.
        """
        resp_bool: bool = os.path.exists(os.path.join(self.path, name))
        return resp_bool
