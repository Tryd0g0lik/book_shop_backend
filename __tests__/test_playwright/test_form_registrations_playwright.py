# __tests__/test_playwright/tests_form_registrations_playwright.py:1
import asyncio
import datetime
import logging
import re
from typing import Optional

import pytest

from __tests__.fixtures.fixture_django3 import TEST_FORM_DATA
from __tests__.test_playwright.playwright_client import PlaywrightManager

pathname_local = "__tests__/test_playwright/screenshots/"
url_star = "http://127.0.0.1:8000/register/admin"
log = logging.getLogger(__name__)


def fixture_add_id_attribute():
    for i in range(0, len(TEST_FORM_DATA)):
        TEST_FORM_DATA[i]["id"] = i + 1


fixture_add_id_attribute()


class TestFormRegistrationsPlaywright:

    @pytest.mark.skip("Нужен код для работы с request и status_code 400 ")
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user_registrate_playwright",
        TEST_FORM_DATA,
        ids=[tc["id"] for tc in TEST_FORM_DATA],
    )
    async def test_form_registrations_playwright(self, user_registrate_playwright):
        log_t = f"[{self.__class__.__name__}][{self.test_form_registrations_playwright.__name__}]:"

        user_data = user_registrate_playwright["data"]
        id = user_registrate_playwright["id"]
        date_screen = re.sub(
            r"[ -:]+", "", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        url_star_list = url_star.split("/")
        client = PlaywrightManager()
        pathname_of_screenshort = "_to_".join(url_star_list[-3:])

        async with client.get_page_acontext_manager(log_t) as page:
            try:
                pass
                # page = await browsers.new_page()
                await page.goto(url_star, wait_until="load")
                #
                form_html = await page.query_selector("form")
                input_type_email = await form_html.query_selector('input[type="email"]')
                await input_type_email.fill(user_data["email"])
                input_name_firstname = await form_html.query_selector(
                    'input[name="first_name"]'
                )
                await input_name_firstname.fill(user_data["first_name"])
                input_name_username = await form_html.query_selector(
                    'input[name="username"]'
                )
                await input_name_username.fill(user_data["username"])
                input_name_password1 = await form_html.query_selector(
                    'input[name="password1"]'
                )
                await input_name_password1.fill(user_data["password1"])
                input_name_password2 = await form_html.query_selector(
                    'input[name="password2"]'
                )
                await input_name_password2.fill(user_data["password2"])
                input_name_check_user = await form_html.query_selector(
                    'input[name="check_user"]'
                )
                await input_name_check_user.click()
                await asyncio.sleep(1)
                await page.screenshot(
                    path=f"{pathname_local}{pathname_of_screenshort}_full_form_{date_screen}_userID_{id}.png",
                    timeout=1000,
                )
                submit_buttom = await form_html.query_selector('button[type="submit"]')
                await submit_buttom.click()
                await asyncio.sleep(10)

                url_star_new = url_star.replace("admin/", "").strip()

                try:
                    await page.wait_for_url(url_star_new, timeout=1000)
                    error_message = await page.query_selector(".errorlist")
                    if error_message:

                        log.warning(f"{log_t} DEBUG JAVASCRIPT result: {error_message}")
                        field_name = TEST_FORM_DATA[id]["expected"]["error_field"]
                        assert TEST_FORM_DATA[id]["expected"]["valid"] in (False,)
                    else:
                        assert TEST_FORM_DATA[id]["expected"]["valid"] in (
                            True,
                        ), "It was checked and data is correct."
                except TimeoutError:
                    assert TEST_FORM_DATA[id]["expected"]["valid"] in (
                        False,
                    ), "It was checked and data is correct."
                    result: Optional[str] = await page.evaluate("""
                    () => {
                        const inputHtmlArray = Array.from(querySelectorALL("input")).map( item => item.border.color === "#00a885");
                        if (inputHtmlArray.length >= 1){
                            const name = inputHtmlArray[0].getAttribute('name');
                            return name;
                        }
                        return null;
                    }
                    """)
                    log.warning(f"{log_t} DEBUG JAVASCRIPT result: {result}")
                    field_name = TEST_FORM_DATA[id]["expected"]["error_field"]
                    assert (
                        result == field_name
                    ), f"The name of the form's field where we see data is not correct: {field_name}"
            finally:
                log.info(f"{log_t} Data ID: {id} completed")
                await page.screenshot(
                    path=f"{pathname_local}{pathname_of_screenshort}_after_submit_{date_screen}_userID_{id}.png",
                    timeout=1000,
                )
                pass
