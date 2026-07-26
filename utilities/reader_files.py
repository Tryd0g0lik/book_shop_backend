# utilities/reader_files.py:1
import base64
import logging
import zipfile
from base64 import decode
from io import BytesIO
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def read_file_safe(file_path: str | Path, file_name, prefix_log=""):
    PREFIX_LOG = (
        "{}[{}]:".format(prefix_log, read_file_safe.__name__)
        if len(prefix_log) == 0
        else "[{}]:".format(read_file_safe.__name__)
    )
    reader = None
    expantion_of_file = file_name.split(".")[-1]
    if expantion_of_file == "xls":
        # .xls (Old Excel 97-2003)
        try:
            reader = pd.read_excel(file_path.name, engine="xlrd")
        except Exception as e:
            log.error(
                "{} Reader engine='xlrd' Error reading file {} =>  {}".format(
                    PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
                )
            )
            try:
                reader = pd.read_excel(file_path.name, engine="openpyxl")
            except Exception as e:
                log.error(
                    "{} Reader engine='openpyxl' Error reading file {} =>  {}".format(
                        PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
                    )
                )
                try:
                    reader = pd.read_excel(file_path)
                except Exception as e:
                    error_t = (
                        "{} Reader engine=None Error reading file {} =>  {}".format(
                            PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
                        )
                    )
                raise ValueError(error_t) from e
    elif expantion_of_file == "xlsx":
        # # .xlsx (Excel 2007+)
        # with open(file_path, "r+") as f:
        #     f.write(file_path)

        try:

            reader = file_path.open(mode="rb").read()  # engine="openpyxl"

        except Exception as e:
            log.error(
                "{} Reader engine=None Error reading file {} =>  {}".format(
                    PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
                )
            )
            try:
                reader = zipfile.ZipFile(file_path.open(), "r")
            except zipfile.BadZipFile as e:
                error_t = "{} Reader ZIP reading file {} =>  {}".format(
                    PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
                )
                log.error(error_t)
            except Exception as e:
                error_t = "{} Reader engine=None Error reading file {} =>  {}".format(
                    PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
                )
                log.error(error_t)

                #
                log.error(error_t)
                raise ValueError(error_t) from e
    else:
        try:
            reader = pd.read_excel(
                file_path,
            )
        except Exception as e:
            error_t = "{} Reader engine=None Error reading file {} =>  {}".format(
                PREFIX_LOG, file_name, e.args[0] if e.args else str(e)
            )
            log.error(error_t)

            raise ValueError(error_t) from e
    log.info("{} File '{}' read.".format(PREFIX_LOG, file_name))
    return reader
