# __tests__/test_playwright/playwright_client.py:1
import logging
from contextlib import asynccontextmanager, contextmanager
from typing import Optional

import playwright.async_api
from playwright.async_api import Browser, async_playwright
from playwright.sync_api import Browser as Sync_Browser
from playwright.sync_api import sync_playwright

from project.settings_conf.settings_env import HEADLESS_MODE

log = logging.getLogger(__name__)
browser_option = {
    "headless":HEADLESS_MODE,
    "args":[
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",  # полезно для Docker/CI
        "--no-sandbox",  # необходимо для некоторых Linux окружений
        "--disable-setuid-sandbox",
        "--disable-gpu",  # отключает GPU (ускоряет headless)
        "--disable-software-rasterizer",
    ]
}

class PlaywrightManager():
    def __init__(self):
        self.async_playwright: Optional[async_playwright] = None
        self.sync_playwright: Optional[sync_playwright] = None
        self.abrowser: Optional[Browser] = None
        self.browser: Optional[Sync_Browser] = None


    def __new__(cls, *args, **kwargs):
        initiakize = super().__new__(cls, *args, **kwargs)
        initiakize.log_t = f"[{cls.__class__.__name__}]:"
        return initiakize

    def __start(self, log_t: str) -> None:
        log_t += f"{log_t[:-1]}[{self.__start.__name__}]:"
        try:
            playwright = sync_playwright()
            p = playwright.start()
            self.browser: Sync_Browser = p.firefox.launch(**browser_option)
            log.info(log_t + " Run the playwright chromium")
        except Exception as e:
            error_t = log_t + e.args[0] if e.args else str(e)
            log.error(error_t)
            raise e

    async def __astart(self, log_t: str) -> None:
        log_t += f"{log_t[:-1]}[{self.__astart.__name__}]:"
        try:
            playwright = async_playwright()
            p = await playwright.start()
            self.abrowser = await p.firefox.launch(**browser_option)
            log.info(log_t + " Run the playwright chromium")
        except Exception as e:
            error_t = log_t + e.args[0] if e.args else str(e)
            log.error(error_t)
            raise e

    @contextmanager
    def get_page_context_manager(self, log_t: str) -> Browser.new_page:
        """
        TODO: https://playwright.dev/python/docs/api/class-apirequestcontext#api-request-context-get
             надо получить статус код из запроса
        :param log_t:
        :return:
        """
        log_t += f"{log_t[:-1]}[{self.get_page_context_manager.__name__}]: "
        self.__start(log_t)

        context: Sync_Browser.new_context = self.browser.new_page(
            userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            xtraHTTPHeaders={
                "Accept-Language": "en-US,en;q=0.9",
            },
            acceptDownloads=False,
            viewport={"width": 1280, "height": 720},
            ignoreHTTPSErrors=True,
            bypassCSP=True,
            timezoneId="Asia/Krasnoyarsk",
        )
        page: playwright.sync_api.Page = context.new_page()
        page.route("**/*kaspersky", lambda route: route.abort())
        page.route("**/*gc.kis.v2.scr*", lambda route: route.abort())
        try:
            yield page
        except Exception as e:
            error_t = log_t + f" {e.args[0] if e.args else str(e)}"
            log.error(error_t)
            raise e
        finally:
            if page:
                page.close()
                log.info(log_t + " Closed the page")
            if context:
                context.close()
                log.info(log_t + " Closed the context")
            self.sync_stop(log_t)

    @asynccontextmanager
    async def get_page_acontext_manager(self, log_t: str) -> Browser.new_page:
        log_t += f"{log_t[:-1]}[{self.get_page_acontext_manager.__name__}]: "
        await self.__astart(log_t)
        context: Browser.new_context = await self.abrowser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
            },
            accept_downloads=False,
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True,
            bypass_csp=True,
            timezone_id="Asia/Krasnoyarsk",
        )
        page: playwright.async_api.Page = await context.new_page()
        await page.route("**/*kaspersky", lambda route: route.abort() )
        await page.route("**/*gc.kis.v2.scr*", lambda route: route.abort())
        try:
            yield page
        except Exception as e:
            error_t = log_t + f" {e.args[0] if e.args else str(e)}"
            log.error(error_t)
            raise e
        finally:
            if page:
                await page.close()
                log.info(log_t + " Closed the page")
            if context:
                await context.close()
                log.info(log_t + " Closed the context")
            await self.async_stop(log_t)

    async def async_stop(self, log_t: str) -> None:
        log_t += f"{log_t[:-1]}[{self.async_stop.__name__}]:"
        if self.abrowser:
            self.abrowser.close()
            log.info(f"{log_t} Browser closed")
        if self.async_playwright:
            self.async_playwright.stop()
        log_t += f"{log_t[:-1]} closed successfully!"

    def sync_stop(self, log_t: str) -> None:
        log_t += f"{log_t[:-1]}[{self.sync_stop.__name__}]:"
        if self.browser:
            self.browser.close()
            log.info(f"{log_t} Browser closed")
        if self.sync_playwright:
            self.sync_playwright.stop()
        log_t += f"{log_t[:-1]}[{self.async_playwright.__name__}]: closed successfully!"
