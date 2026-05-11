# import logging
# from pathlib import Path
#
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IS_DEBUG = os.getenv("IS_DEBUG", "1")
DEBUG = True if int(IS_DEBUG) == 1 else False
# logging.basicConfig(filename=f"{DIR_NAME}/log_putout.log", level=logging.INFO)
