# download/task_save_file.py:1
import asyncio
import json
import logging
import os
import queue
import re
import threading
from datetime import datetime

import pandas as pd

from project import settings
from project.settings_conf.settings_first import DEFAULT_CHARSET

log = logging.getLogger(__name__)
PATH_ERROR_DIR = os.path.join(settings.MEDIA_ROOT, "error_catalog")
TEMPLATE_NAME_OF_FILES = r"(^product_error_[0-9-_]+\.txt)$"
CHECKLIST = [
    "product_name",
    "describe_preview",
    "description",
    "price",
    "discount_percent",
    "stock_quantity",
]
MAX_FILE_SIZE = 200 * 1024

q = queue.Queue(maxsize=2000)


async def write_error_data(q: queue, view_list: list) -> None:
    """

    :param q: queue. When will be writing if The data don't save in database.
    :param view_list: IT is data which will be  saving. Zero index it is a key. Second it is a value/
        This list hase a length to 2 (index 0 & index 1)/
    :return: void
    """
    try:
        q.put_nowait(
            json.dumps(
                {view_list[0].strip(): str(view_list[1]).strip()}, ensure_ascii=False
            )
        )
    except queue.Full:
        await asyncio.wait_for(
            asyncio.to_thread(
                lambda: q.put(
                    json.dumps(
                        {view_list[0].strip(): str(view_list[1]).strip()},
                        ensure_ascii=False,
                    )
                )
            ),
            30,
        )


# ============================================
# TASK IS FOR SAVING DATA OF FILE IN DATABASE.
# ============================================
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


async def subprocess_data(data: pd.array):
    from catalog.models import (
        BrandModel,
        CategoryModel,
        ProductCharacteristics,
        ProductModel,
    )

    lock = asyncio.Lock()
    # Keys of file
    keys = list(data.keys())
    checklist: list[str] = [item for item in keys if item in CHECKLIST]
    if len(checklist) < 4:
        return
    # Values
    values = list(data.values)
    shape = data.shape
    for view_list in values:
        product = ProductModel()
        index_key = keys.index("is_active")
        product.is_active = view_list[index_key]
        for index in range(0, shape[1] - 1):
            k = None
            v = None
            # ============================================
            # CREATE PRODUCT IN DATABASE
            # ============================================
            k = keys[index]

            v = view_list[index]
            try:
                if k == "product_name":
                    setattr(product, "name", v)
                    continue
                elif re.search(r"^brand_", k):
                    try:
                        if type(v) == int:
                            await BrandModel.objects.aget(pk=int(v))
                        elif type(v) == str:
                            result = await BrandModel.objects.aget(name=v)
                            v = result.id
                    except Exception:
                        num_desc = keys.index("brand_description")
                        num_key = keys.index("brand_name")
                        brand_unknown = await BrandModel.objects.acreate(
                            name=view_list[num_key], description=view_list[num_desc]
                        )
                        v = brand_unknown.id
                    setattr(product, "brand_id", v)
                    continue
                elif re.search(r"^category_", k):
                    try:
                        if type(v) == int:
                            await CategoryModel.objects.aget(pk=v)
                        elif type(v) == str:
                            result = await CategoryModel.objects.aget(name=v)
                            v = result.id
                    except Exception:
                        num_desc = keys.index("category_description")
                        num_key = keys.index("category_name")
                        category_unknown = await CategoryModel.objects.acreate(
                            name=view_list[num_key], description=view_list[num_desc]
                        )
                        v = category_unknown.id
                    setattr(product, "category_id", v)
                    continue
                elif k == "attributes_additional":
                    v_list = v.split(",")
                    v_dict = dict()
                    for view_str in v_list:
                        view_str = re.sub(r"[}{]+", "", view_str)
                        l: list | str = view_str.split(":")
                        l = l.split("=") if type(l) == str else l

                        v_dict.setdefault(l[0], l[1])
                    setattr(product, "attributes_additional", v_dict)
                    continue
                elif k != "attributes":
                    setattr(product, k, v)
                    continue
                else:
                    continue
            except Exception as e:
                log.error(
                    "[subprocess_data]: Error => {}".format(
                        e.args[0] if len(e.args) > 0 else str(e)
                    )
                )

                await write_error_data(q, [k, v])
                continue
        async with lock:
            # ============================================
            # CREATE POSITIONS IN DATABASE
            # ============================================
            try:

                await product.asave()
            except Exception as e:
                log.warning(
                    f"[subprocess_data]: It seems this product was created before that. WARNING => {
                    e.args[0] if len(e.args) > 0 else str(e)
                    }"
                )
                await write_error_data(q, [k, v])
                continue

                # ============================================
                # CREATE CHARACTERISTICS OF PRODUCT IN DATABASE
                # ============================================
            if keys.count("attributes") > 0:
                number = keys.index("attributes")

                result: list[str] = view_list[number].split(",")
                view_list: list[str] = [result] if type(result) == str else result
                for item in view_list:
                    item_list: list[str] | str = (
                        item.split(":")
                        if type(item) == str and "=" not in item
                        else item.split("=")
                    )

                    v_list = [item.strip() for item in item_list]
                    try:
                        tasks_collection = []
                        for i in range(0, len(v_list)):
                            if i % 2 != 0:
                                continue
                            tasks_collection.append(
                                asyncio.create_task(
                                    ProductCharacteristics.objects.acreate(
                                        name=v_list[0].strip(),
                                        value=v_list[1].strip(),
                                        product_id=product.id,
                                    )
                                )
                            )
                        await asyncio.gather(*tasks_collection)
                    except Exception as e:
                        log.error(
                            "[subprocess_data]: Error => {}".format(
                                e.args[0] if len(e.args) > 0 else str(e)
                            )
                        )
                        await write_error_data(q, v_list)
                        continue
    await storage_errors(q)


# ============================================
# STORAGE A LOST DATA
# ============================================
async def storage_errors(q: queue.Queue):
    queue_data = None
    # ---
    f = Files(PATH_ERROR_DIR)
    try:
        while not q.empty():
            try:
                queue_data = q.get_nowait()

            except Exception as e:
                log.error(
                    "[storage_errors]: {}".format(
                        e.args[0] if len(e.args) > 0 else str(e)
                    )
                )
                return

            # Search an empty file
            # Check file, it is full or empty
            empty_file = f.get_empty_file()
            # ---
            s = f"{json.dumps(queue_data, ensure_ascii=False)}\n"
            # If Files was found
            if empty_file is not None:
                # for name in files_name:
                path_full = os.path.join(f.path, empty_file)

                # If full
                with open(path_full, "r+", encoding=DEFAULT_CHARSET) as file:
                    text_old = file.read()
                    if len(text_old) == 0:
                        file.write(s)
                    else:
                        # text_new = f"{text_old}{s}"
                        file.write(s)
            else:
                # If files not found
                i = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                with open(
                    os.path.join(f.path, f"product_error_{i}.txt"),
                    "w+",
                    encoding=DEFAULT_CHARSET,
                ) as file:
                    file.write(s)
    except queue.Empty:
        log.warning("[storage_errors]: Queue is empty")
        return
    except Exception as e:
        log.error(
            "[storage_errors]: ERROR => {}".format(
                e.args[0] if len(e.args) > 0 else str(e)
            )
        )


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
