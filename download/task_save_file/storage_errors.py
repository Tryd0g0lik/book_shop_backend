# download/task_save_file/storage_errors.py:1
import asyncio
import json
import logging
import os
import queue
from datetime import datetime

from download.task_save_file.files_objects import PATH_ERROR_DIR, Files
from project.settings_conf.settings_first import DEFAULT_CHARSET

log = logging.getLogger(__name__)


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
                {
                    view_list[0].strip(): {
                        "product_name": str(view_list[2]).strip(),
                        "value": str(view_list[1]).strip(),
                    }
                },
                ensure_ascii=False,
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
