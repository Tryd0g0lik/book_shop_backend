# persons/tasks/tasks_celery/task_create_position/create_position_allauth.py:1
# Adding of positions to the Alliauth's  EmailAddress & EmailConfirmation
# This task run after an event of login
import asyncio
import logging
from typing import Optional

from persons.interfaces import EmailAddress as AllauthEmailAddress
from persons.tasks.tasks_celery.task_create_position.functions import (
    aget_object_from_allauth_or_log,
    aget_object_of_log,
)

log = logging.getLogger(__name__)


async def create_some_position_allauth(*args, **kwargs: dict[str, int]) -> None:
    """
    TODO: EmailAddress 'verified' имеет False после авторизации
    :param args: -
    :param kwargs: "{'user_id':int, 'timeout_server':int}"
    :return: None
    """

    from allauth.account.models import EmailAddress

    from persons.models import Users as UsersModel

    if kwargs is None or len(dict(kwargs).keys()) == 0:
        return None
    log_t = f"[{create_some_position_allauth.__name__}]:"
    try:
        # number of user that just  now created (in process) account
        user_id: Optional[int] = kwargs.get("user_id")
        # number of seconds
        timeout_server: Optional[int] = kwargs.get("timeout_server")
        if (
            user_id is None
            or timeout_server is None
            or user_id < 0
            or timeout_server < 0
        ):
            log.warning(
                log_t
                + f" 'user_id' or 'timeout_server' is incorrect! args: {str(args)} & kwargs: {str(kwargs)}"
            )
            return None
        # Getting obj of last of user for will add of positions to the Alliauth's  EmailAddress & EmailConfirmation
        user: UsersModel | None = await aget_object_of_log(UsersModel, user_id, log_t)
        if user is None:
            return None
        # --- Allauth EmailAddress
        account_email: AllauthEmailAddress | None = await aget_object_of_log(
            EmailAddress, user.pk, log_t
        )
        if account_email is None:
            return None
        if not account_email.verified:
            setattr(account_email, "verified", True)

            asave = account_email.asave
            try:
                await asyncio.wait_for(
                    asave(update_fields=["verified"]), timeout_server
                )
            except asyncio.TimeoutError:
                log.warning(
                    log_t
                    + " TimeoutError data didn't update in the 'EmailAddress' database!"
                )
                return None
            except Exception as e:
                log.warning(log_t + " ERROR => " + e.args[0] if e.args else str(e))
                return None
        else:
            # Allauth
            log.info(log_t + " has exists 'verified' in database!")
            return None

        # --- Allauth EEmailConfirmation
        email_obj = await aget_object_from_allauth_or_log(account_email.pk, log_t)

        if email_obj is None:
            return None
        if not email_obj.verified:
            email_obj.verified = True
            try:
                await asyncio.wait_for(email_obj.asave(), timeout_server)
            except asyncio.TimeoutError:
                log.warning(log_t + " TimeoutError data didn't update in database!")
                return None
            except Exception as e:
                log.warning(log_t + " ERROR => " + e.args[0] if e.args else str(e))
                return None

        else:
            log.info(log_t + "Allauth did not save new email!")
            return None
    except Exception as e:
        log.warning("{} ERROR => {}".format(log_t, e.args[0] if e.args else str(e)))
