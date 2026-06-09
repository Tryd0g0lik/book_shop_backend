# __tests__/test_playwright/tests_form_registrations_playwright.py:1
import asyncio
import datetime
import logging
import re

import pytest
from playwright.async_api import (
    Page,
    Playwright,
    async_playwright,
)

from __tests__.fixtures.fixture_django3 import TEST_FORM_DATA

pathname_local = "__tests__/test_playwright/screenshots/"
url_star = "http://127.0.0.1:8000/register/admin/"


# class TestFormRegistrationsPlaywright:
@pytest.fixture
async def browsers():
    """Open a browser"""
    async with async_playwright() as p:
        webkit = p.chromium
        browser = await webkit.launch()
        context = await browser.new_context()
        yield context
        await context.close()
        await browser.close()

@pytest.mark.parametrize("user_registrate_playwright", TEST_FORM_DATA, ids=[tc["id"] for tc in TEST_FORM_DATA])
async def test_form_registrations_playwright( user_registrate_playwright):
    user_data = user_registrate_playwright["data"]
    id = user_registrate_playwright["id"]
    date_screen = re.sub(r"[ -:]+", "", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    url_star_list = url_star.split("/")
    pathname_of_screenshort = "_to_".join(url_star_list[-3:])
    async with async_playwright() as p:
        webkit = p.chromium
        browser = await webkit.launch()
        context = await browser.new_context()
        page = await context.new_page()
        try:

            await page.goto(url_star, wait_until="load")

            form_html = await page.query_selector("form")
            input_type_email = await form_html.query_selector('input[type="email"]')
            await input_type_email.fill(user_data["email"])
            input_name_firstname = await form_html.query_selector('input[name="first_name"]')
            await input_name_firstname.fill(user_data["first_name"])
            input_name_username = await form_html.query_selector('input[name="username"]')
            await input_name_username.fill(user_data["username"])
            input_name_password1 = await form_html.query_selector('input[name="password1"]')
            await input_name_password1.fill(user_data["password1"])
            input_name_password2 = await form_html.query_selector('input[name="password2"]')
            await input_name_password2.fill(user_data["password2"])
            input_name_check_user = await form_html.query_selector('input[name="check_user"]')
            await input_name_check_user.click()
            await asyncio.sleep(1)
            await page.screenshot(path=f"{pathname_local}{pathname_of_screenshort}_full_form_{date_screen}_id_user{id}.png", timeout=5)
            submit_buttom = await form_html.query_selector('button[type="submit"]')
            await submit_buttom.click()
            await asyncio.sleep(4)
            await page.screenshot(path=f"{pathname_local}{pathname_of_screenshort}_after_submit_{date_screen}.png", timeout=5)
            url_star_new = url_star.replace("admin/", "").strip()
            try:
                await page.wait_for_url(url_star_new, timeout=4)
                assert True, "The page for checks of code verification was  uploaded."
            except TimeoutError:
                assert False, "The page for checks of code verification hase not uploaded"

        finally:
            await page.close()
            await context.close()
            await browser.close()
