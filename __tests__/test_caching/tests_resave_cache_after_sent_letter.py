import asyncio
import json
import logging
import re

from allauth.account.internal.userkit import user_email

from __tests__.fixtures.fixture_django2 import pytest_generate_tests
from persons import EnumTemplatesKeysCache

log = logging.getLogger(__name__)



class TestResaveCacheAfterSentLetter:
    async def test_resave_cache_after_sent_letter(self, new_users_registration):
        from persons.services import AccountManager

        log_t = "TEST" + f"[{self.test_resave_cache_after_sent_letter.__name__}]:"
        account_manager = AccountManager()
        postman = account_manager.postman
        SubPerson = postman.SubPerson
        sub_person = SubPerson()
        cachemanager = sub_person.cachemanager
        await sub_person.cachemanager.asynccacher.related()
        k1 =re.sub(r'[@.]+', repl="", string=f"user:pending:{new_users_registration["email"]}", flags=re.ASCII)
        k2 = re.sub(r'[@.]+', repl="", string=f"user:pending:letter:{new_users_registration["email"]}", flags=re.ASCII)
        assert k1.count(":") == 2
        assert k2.count(":") == 3

        keys = [k1]
        tasks = []
        username_ = new_users_registration.get("username")
        user_email_ = new_users_registration.get("email")
        await cachemanager.asave(key=k1, default={"username": username_, "email": user_email_})

        async def resave_cache_after_sent_letter(*args) -> bool:
            """
            Test property is a basis check logic
            :param str args: It is the one old key of cache.
            persons/tasks/tasks_celery/task_send_letter_to_user_email.py:130
            :return:
            """
            lt = "TEST" + f"[{resave_cache_after_sent_letter.__name__}]:"
            for k in args:
                assert type(k) == str
                assert k.count(":") == 2
                data_list: list = []
                try:
                    # It is receiving the user data
                    await cachemanager.aget(key=k, collection=data_list, exat=1)
                    assert len(data_list) == 1

                    # New key for resaves
                    key: str = (
                        EnumTemplatesKeysCache.USER_PENDING_LETTER.value
                        % k.split(":")[-1]
                    )
                    assert k2 == key
                    user_data_json: dict =json.loads((data_list[0]).decode("utf-8"))

                    # Re-save
                    response_bool = await cachemanager.asave(key=key, default=user_data_json, ttl=300)
                    log.info(
                        lt
                        + f"User dada Re-saved successfully from old {args} key !"
                    )
                    assert type(response_bool) in (bool,)
                    assert response_bool in (True,)
                    return response_bool

                except Exception as e:
                    log.error(lt + " ERROR => " + e.args[0] if e.args else str(e))
                    return False
            return True
        for key in keys:

            tasks.append(resave_cache_after_sent_letter(*(key,)))
        await asyncio.gather(*tasks, return_exceptions=True)

        data_list =[]
        result_bool = await cachemanager.aget(key=k2, collection=data_list, ex=1300)
        assert len(data_list) > 0
        assert result_bool in (True,)

        assert type(data_list) in (list,)
        assert len(data_list) == 1
        result_bool = await cachemanager.aget(key=k1, collection=data_list, )
        assert result_bool is None
