"""
persons/adapters/__init__.py:1
"""

__all__ = ["CacherAdapterMixin", "AsyncCacherAdapterMixin"]

from persons.adapters.async_cache_adapter import AsyncCacherAdapterMixin
from persons.adapters.cache_adapter import CacherAdapterMixin
