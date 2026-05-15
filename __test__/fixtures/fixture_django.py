"""
__test__/fixtures/fixture_django.py:1
"""

import pytest


@pytest.fixture(scope="session")
def django_setup():
    import os

    import django

    """Однократная настройка Django для всех тестов"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    return True
