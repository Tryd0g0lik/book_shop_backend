import pytest


@pytest.fixture
def fixture_cacher_adapter_mixin():
    from utilities.adapters import CacherAdapter

    test_cacher = CacherAdapter()
    CacherAdapter._pool = None
    yield test_cacher
    if test_cacher.is_connected:
        test_cacher.close()
