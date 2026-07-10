# persons/tasks/tasks_celery/task_create_position/create_position_wagtail_profile.py:1
import asyncio
import logging
from typing import Optional

from allauth.account.models import EmailConfirmation

log = logging.getLogger(__name__)


async def create_some_position_at_wagtail_profile(
    *args, **kwargs: dict[str, int]
) -> None:
    """
    :param args: -
    :param kwargs: "{'user_id':int, 'timeout_server':int}"
    :return: None
    """
    from wagtail.users.models import UserProfile

    from persons.models import Users

    log_t = f"[{create_some_position_at_wagtail_profile.__name__}]:"
    # number of user that just  now created (in process) account
    user_id: Optional[int] = kwargs.get("user_id")
    # number of seconds
    timeout_server: Optional[int] = kwargs.get("timeout_server")
    if user_id is None or timeout_server is None or user_id < 0 or timeout_server < 0:
        log.warning(
            log_t
            + f" 'user_id' or 'timeout_server' is incorrect! args: {str(args)} & kwargs: {str(kwargs)}"
        )
        return None
    try:
        user = await Users.objects.aget(id=user_id)
        if user:
            try:
                await asyncio.wait_for(
                    UserProfile.objects.aget_or_create(user=user),
                    timeout=timeout_server,
                )
            except asyncio.TimeoutError:
                log.warning(
                    log_t
                    + " TimeoutError data didn't update in the 'wagtail.users.UserProfile' database!"
                )
                return None
            except Exception as e:
                log.warning(log_t + " ERROR => " + e.args[0] if e.args else str(e))
                return None
    except EmailConfirmation.DoesNotExist:
        log.error(log_t + " 'user' not exists in database!")
        return None
