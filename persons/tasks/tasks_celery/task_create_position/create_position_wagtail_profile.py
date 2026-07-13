# persons/tasks/tasks_celery/task_create_position/create_position_wagtail_profile.py:1
import asyncio
import logging
from typing import Optional

from allauth.account.models import EmailConfirmation
from django.db.models import QuerySet

from persons.tasks.tasks_celery.task_create_position.functions import (
    aget_object_of_log,
    greate_of_profile,
)
from utilities import CATEGORY_STATUS

log = logging.getLogger(__name__)


async def create_some_position_at_wagtail_profile(
    *args, **kwargs: dict[str, int]
) -> None:
    """
    :param args: -
    :param kwargs: "{'user_id':int, 'timeout_server':int}"
    :return: None
    """
    from wagtail.users.models import UserProfile as WagtailUserProfile

    from persons.interfaces import Users as UsersInterface
    from persons.models import Users
    from profiles.models import (
        AdminProfileModel,
        ClientProfileModel,
        EditorProfileModel,
        ManagerProfileModel,
        ModeratorProfileModel,
    )

    log.info("WAGTAIL  DEBUG 0")
    log_t = f"[{create_some_position_at_wagtail_profile.__name__}]:"
    # number of user that just  now created (in process) account
    user_id: Optional[int] = kwargs.get("user_id")
    # number of seconds
    timeout_server: Optional[int] = kwargs.get("timeout_server")
    if user_id is None or timeout_server is None or user_id < 0 or timeout_server < 0:
        log.warning(
            log_t
            + f" 'user_id': {user_id} or 'timeout_server': {timeout_server} is incorrect! args: {str(args)} & kwargs: {str(kwargs)}"
        )
        return None
    log.info("WAGTAIL  DEBUG 1")
    # 'Users' model from the 'person.models.model_persons.Users'
    user: UsersInterface = await aget_object_of_log(Users, user_id, log_t)
    if user is None:
        return None
    log.info("WAGTAIL  DEBUG 2")
    try:
        wagtail_user_profile_obj, wagtail_user_bool = await asyncio.wait_for(
            WagtailUserProfile.objects.aget_or_create(user=user),
            timeout=timeout_server,
        )
        log.info("WAGTAIL  DEBUG 3")
        # if not wagtail_user_bool:
        #     log.warning(
        #         "{} User not found at the Wagtail's profile of user".format(log_t)
        #     )
        #     return None

        # group_name: str = user.groups.values_list("name", flat=True)
        # if group_name.lower() == CATEGORY_STATUS[1][0].lower():
        #     # admin
        log.info("WAGTAIL  DEBUG 4")

        await greate_of_profile(
            [
                ManagerProfileModel,
                AdminProfileModel,
                EditorProfileModel,
                ClientProfileModel,
                ModeratorProfileModel,
            ],
            wagtail_user_profile_obj,
            log_t[:-1],
        )
        log.info("WAGTAIL  DEBUG 5")
        pass
    except asyncio.TimeoutError:
        log.warning(
            log_t
            + " TimeoutError data didn't update in the 'wagtail.users.UserProfile' database!"
        )
        log.info("WAGTAIL  DEBUG 6")
        return None
    except Exception as e:
        log.info("WAGTAIL  DEBUG 7")
        log.warning(log_t + " 000 ERROR => " + e.args[0] if e.args else str(e))
        return None
