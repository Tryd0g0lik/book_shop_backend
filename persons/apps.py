import logging
import os
import sys

from django.apps import AppConfig
from django.dispatch import Signal

from utilities.services import AccountManager, CacheManager

# from persons.services.person_manager import PersonManager

# from pathlib import Path
# DJANGO_SETTINGS_MODULE="project.settings"
# BASE_DIR = Path(__file__).resolve().parent.parent
IS_DEBUG = os.getenv("IS_DEBUG", "1")
DEBUG = True if int(IS_DEBUG) == 1 else False

# personmanager = PersonManager()
cachemanager = CacheManager()
account_manager = AccountManager()
new_person_signal = Signal(use_caching=False)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] %(levelname)s - %(name)s:%(lineno)d -  [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)


class PersonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "persons"
