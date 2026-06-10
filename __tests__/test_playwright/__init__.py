# __tests__/test_playwright/__init__.py:1
import asyncio
import sys

if sys.platform == "win32":
    # https://docs.python.org/3.13/library/asyncio-platforms.html#subprocess-support-on-windows !!!
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
