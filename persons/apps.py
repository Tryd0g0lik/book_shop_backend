import os

from django.apps import AppConfig
from django.dispatch import Signal

from persons.services.person_manager import PersonManager

# from pathlib import Path


# DJANGO_SETTINGS_MODULE="project.settings"

# BASE_DIR = Path(__file__).resolve().parent.parent
IS_DEBUG = os.getenv("IS_DEBUG", "1")
DEBUG = True if int(IS_DEBUG) == 1 else False

personmanager = PersonManager()

new_person_signal = Signal(use_caching=False)


class PersonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "persons"
