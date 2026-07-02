# download/task_save_file/subprocess.py:1
import asyncio
import logging
import queue
import re

import pandas as pd

from download.task_save_file.storage_errors import storage_errors, write_error_data

q = queue.Queue(maxsize=2000)
CHECKLIST = [
    "product_name",
    "describe_preview",
    "description",
    "price",
    "discount_percent",
    "stock_quantity",
]
log = logging.getLogger(__name__)


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
