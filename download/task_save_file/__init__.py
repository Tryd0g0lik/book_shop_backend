# download\task_save_file\__init__.py
# ============================================
# TASK IS FOR SAVING DATA OF FILE IN DATABASE.
# ============================================
import asyncio
import base64
import logging
import os
import re
import threading
from io import BytesIO
from pathlib import Path

import pandas as pd

from download.task_save_file.subprocess import subprocess_data
from project import BASE_DIR
from utilities.reader_files import read_file_safe

log = logging.getLogger(__name__)


def task_saving_data_oFfile(*args, **kwargs):
    global reader
    PREFIX_LOG = "[{}]:".format(task_saving_data_oFfile.__name__)
    file_name: str = list(args)[0]
    print(file_name)
    if not file_name:
        return
    path = BASE_DIR / "media" / "documents"

    names_list = os.listdir(path)
    names_list = [item for item in names_list if item == file_name]
    if len(names_list) == 0:
        return
    templ = "\\"
    path = str(path / file_name).replace(templ, "/")
    # path = Path(BASE_DIR) / "media" / "documents" / file_name
    try:
        expantion_of_file = file_name.split(".")[-1]
        # переписать  на open () или сохранять через pandas при этом посмотреть доку .venv/Lib/site-packages/pandas/io/excel/_base.py:198
        # with open(file=path, mode="rb", ) as f:
        #     reader = base64.b64decode(f.read())
        # reader = read_file_safe(path, file_name, PREFIX_LOG[:-1])
        if expantion_of_file == "xls":
            with pd.ExcelFile(path, engine="xlrd") as excel:
                reader = pd.read_excel(excel)
        elif expantion_of_file == "xlsx":
            with pd.ExcelFile(path, engine="openpyxl") as excel:
                reader = pd.read_excel(excel, engine="openpyxl")

        else:
            return

        def wraper():
            # ---
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(subprocess_data(reader, list(args)[1]))
            return

        threading.Thread(target=wraper).start()
        log.info("{} File '{}' uploaded.".format(PREFIX_LOG, file_name))
        return True
    except Exception as e:
        error_t = "{} File '{}' ERROR => {}.".format(
            PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
        )
        log.error(error_t)

        raise ValueError(error_t)
