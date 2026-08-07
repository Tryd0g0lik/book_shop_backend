# persons/tasks/tasks_celery/task_create_position/create_position_wagtail_profile.py:1
import asyncio
import logging
from typing import Optional

from persons.tasks.tasks_celery.task_create_position.functions import (
    aget_object_of_log,
    greate_of_profile,
)

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
    # 'Users' model from the 'person.models.model_persons.Users'
    user: UsersInterface = await aget_object_of_log(Users, user_id, log_t)
    if user is None:
        return None
    try:
        wagtail_user_profile_obj, wagtail_user_bool = await asyncio.wait_for(
            WagtailUserProfile.objects.aget_or_create(user=user),
            timeout=timeout_server,
        )
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
        pass
    except asyncio.TimeoutError:
        log.warning(
            log_t
            + " TimeoutError data didn't update in the 'wagtail.users.UserProfile' database!"
        )
        return None
    except Exception as e:
        log.warning(log_t + " ERROR => " + list(e.args)[0] if e.args else str(e))
        return None
