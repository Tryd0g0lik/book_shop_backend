import pytest


@pytest.fixture
def fixture_cacher_adapter_mixin():
    from persons.adapters import CacherAdapterMixin
    test_cacher = CacherAdapterMixin()
    CacherAdapterMixin._pool = None
    yield test_cacher
    if test_cacher.is_connected:
        test_cacher.close()
