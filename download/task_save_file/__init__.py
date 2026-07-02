# download\task_save_file\__init__.py
# ============================================
# TASK IS FOR SAVING DATA OF FILE IN DATABASE.
# ============================================
import asyncio
import os
import threading

import pandas as pd

from download.task_save_file.subprocess import subprocess_data


def task_saving_data_oFfile(*args, **kwargs):
    file_name = list(args)[0]
    print(file_name)
    if not file_name:
        return
    path = os.getcwd() + "\\media\\documents\\"
    names_list = os.listdir(path)
    names_list = [item for item in names_list if item == file_name]
    if len(names_list) == 0:
        return
    try:

        def wraper():
            print(path + file_name)
            data = pd.read_excel(path + file_name, engine="xlrd")
            # ---
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(subprocess_data(data))
            return

        threading.Thread(target=wraper).start()
    except Exception as e:
        print(e)
