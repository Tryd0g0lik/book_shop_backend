# download\task_save_file\__init__.py
# ============================================
# TASK IS FOR SAVING DATA OF FILE IN DATABASE.
# ============================================
import asyncio
import logging
import os
import threading

import pandas as pd

from download.task_save_file.subprocess import task_sub_process_data
from project import BASE_DIR

log = logging.getLogger(__name__)


def task_saving_data_oFfile(*args, **kwargs) -> tuple[bool, str]:
    """
    This task save the data of the Excel file.
    :param args: (< file_name >, < user_index >)
    :param kwargs: _
    :return: tuple[bool, str]
    """
    global reader
    PREFIX_LOG = "[{}]:".format(task_saving_data_oFfile.__name__)
    file_name: str = list(args)[0]
    if not file_name:
        return False, "The file does not have a file name"
    path = BASE_DIR / "media" / "documents"
    reader = None
    names_list = os.listdir(path)
    names_list = [item for item in names_list if item == file_name]
    if len(names_list) == 0:
        return False, "The directory does not have files."
    templ = "\\"
    path = str(path / file_name).replace(templ, "/")
    try:
        expantion_of_file = file_name.split(".")[-1]
        if expantion_of_file == "xls":
            # File xls - format
            with pd.ExcelFile(path, engine="xlrd") as excel:
                reader = pd.read_excel(excel)
        elif expantion_of_file == "xlsx":
            # File xlsx format
            with pd.ExcelFile(path, engine="openpyxl") as excel:
                reader = pd.read_excel(excel, engine="openpyxl")
        else:
            return False, "The file hase an incorrect format"
        if reader is not None:

            def wraper():
                # ---
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(
                        task_sub_process_data(reader, list(args)[1])
                    )
                    return True
                except Exception as e:
                    error_t = "{} File '{}' ERROR => {}.".format(
                        PREFIX_LOG, file_name, list(e.args)[0] if e.args else str(e)
                    )
                    log.error(error_t)
                    return False

            threading.Thread(target=wraper).start()
            log.info("{} File '{}' uploaded.".format(PREFIX_LOG, file_name))
            return True, "Success"
        return False, "Not success"
    except Exception as e:
        error_t = "{} File '{}' ERROR => {}.".format(
            PREFIX_LOG, file_name, list(e.args)[0] if e.args else str(e)
        )
        log.error(error_t)

        raise ValueError(error_t)
