
import logging
import re

import pytest
import requests

from utilities.services import AccountManager

log = logging.getLogger(__name__)


class TestRegistrationAndSendCodeVerification:

    # @pytest.fixture(autouse=True)
    # async def close_db_async(self):
    #     yield
    #     from django.db import connection
    #     await asyncio.to_thread(connection.close)

    @pytest.fixture(scope="session")
    def super_form_valid(self):
        # from persons.apps import cachemanager  # account_manager,
        # from persons.tasks.tasks_celery.task_set_cache import cache_user_data
        from persons.interfaces import UsersPydantic

        # from persons.tasks.tasks_celery.task_send_letter_to_user_email import task_postman
        # from persons.tasks.tasks_celery.task_set_cache import (
        #     task_of_cache,
        # )

        account_manager = AccountManager()

        async def async_super_form_valid(user_data):
            from utilities import EnumTemplatesKeysCache
            postman = account_manager.postman
            log.info(f"""\n
            # ============================================
            # MOCK the form_valid
            # user_data: {user_data}
            # ============================================
            """)

            # Create a new user.
            SubPerson = postman.SubPerson
            database_service_ = postman.database_service
            email = user_data.get("email")
            username = user_data.get("username")
            log.info(f"""\n
            # ============================================
            # MOCK the form_valid 2
            # email: {email}
            # username: {username}
            # ============================================
            """)
            sub_person = SubPerson(person_email=email)
            log.info(f"""\n ------------------------------------------------------ \n
            {user_data}
""")
            sub_person.get_person_model = UsersPydantic(**user_data)
            log.info(f"""\n
            # ============================================
            # Make a new cache
            # sub_person.get_person_model: {sub_person.get_person_model}
            # sub_person.get_person_model Type: {type(sub_person.get_person_model)}
            # ============================================
            """)
            value: str = EnumTemplatesKeysCache.USER_PENDING_ZERO.value % re.sub(
                r"[@.]", "", email
            )
            await sub_person.cachemanager.asave(
                value, {"username": username, "email": email}
            )
            log.info(f"""\n
            # ============================================
            # MOCK the form_valid
            # email: {email}
            # Key: {value}
            # ============================================
            """)

            await sub_person.get_model(database_service_, value)
            # await asyncio.to_thread(lambda : sub_person._get_data(value,database_service=database_service_))
            # await cachemanager.asynccacher.close()
            return

        yield async_super_form_valid

    @pytest.fixture
    def requests_logic(
        self,
    ):
        from django.contrib.auth.models import AnonymousUser
        from django.urls import reverse

        def wrapper(new_users_registration):
            test_new_user: dict = {
                k: v
                for k, v in new_users_registration.items()
                if k
                in [
                    "email",
                    "first_name",
                    "username",
                    "password1",
                    "password2",
                    "check_user",
                    "category",
                ]
            }
            url = reverse("persons:management")
            # url = url + "admin" if "admin" not in url else url
            log.info(f"""\n
                    # ============================================
                    # TEST DEBUG POST'S DATA BEFORE SEND
                    # test_new_user: {test_new_user},
                    # ============================================
                    """)
            request = requests.post(
                url="http://127.0.0.1:8000/register/admin",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "http://127.0.0.1:8000/register/admin",
                    "Host": "127.0.0.1:8000",
                    "method": "POST",
                },
                data=test_new_user,
            )
            # request = await client.post(
            #     url,
            #     test_new_user,
            #     follow=True
            # )

            # request.method='POST'
            # request.path='register/admin'
            request.user = AnonymousUser()
            yield request
            # request.close()

        # request._messages = add_message
        return wrapper

    @pytest.mark.parametrize(
        "new_users_registration",
        [
            {
                "id": None,
                "last_login": None,
                "is_superuser": True,
                "username": "admin_super",
                "first_name": "Admin",
                "last_name": "Supervisor",
                "email": "admin@example.com",
                "is_staff": True,
                "is_active": True,
                "date_joined": None,
                "category": "ADMIN",
                "password": "pbkdf2_sha256$hash_admin_1",
                "is_sent": True,
                "is_verified": True,
                "verification_code": "admin_verification_code_123",
                "balance": 0.0,
                "created_at": None,
                "updated_at": None,
            },
            {
                "id": None,
                "last_login": None,
                "is_superuser": False,
                "username": "staff_moderator",
                "first_name": "Moderator",
                "last_name": "Staff",
                "email": "moderator@example.com",
                "is_staff": True,
                "is_active": True,
                "date_joined": None,
                "category": "STAFF",
                "password": "pbkdf2_sha256$hash_staff_2",
                "is_sent": True,
                "is_verified": True,
                "verification_code": None,
                "balance": 0.0,
                "created_at": None,
                "updated_at": None,
            },
        ],
    )
    @pytest.mark.django_db
    async def test_registration_and_send_code_verification(
        self, super_form_valid, new_users_registration, requests_logic, mocker
    ):

        log.info("""\n
        # ============================================
        # MOCK the celery's tasks - task_postman & task_of_cache
        # ============================================
        """)
        await super_form_valid(new_users_registration)
        requests_logic(new_users_registration)
        log.info("""\n
        # ============================================
        # TEST Django's Client a POST request.
        # ============================================
        """)
        # client = AsyncClient(
        #     headers={
        #         'Content-Type': 'application/x-www-form-urlencoded',
        #         'Referer': 'http://127.0.0.1:8000/register/admin/',
        #         'Host': '127.0.0.1:8000',
        #         'method': "POST",
        #     },
        #
        # )
