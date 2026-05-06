import logging
from pathlib import Path

DIR_NAME = Path(__file__).resolve().parent
logging.basicConfig(filename=f"{DIR_NAME}/log_putout.log", level=logging.INFO)
