# persons/tasks/tasks_celery/task_create_position/functions.py:1
# This brought the duplicate cado here from create_position_allauth.py
# Plus the function 'aget_object_of_log' is duplicate ather ways else.

import logging
from typing import NewType, Optional

from allauth.account.models import EmailAddress
from django.http import Http404
from django.shortcuts import aget_object_or_404

from persons.interfaces import EmailConfirmation as AlluathEmailConfirmation
from persons.interfaces import Users

log = logging.getLogger(__name__)

E = NewType["E", EmailAddress]
M = NewType("M", E | Users)


async def aget_object_of_log(
    model: M, user_id: int, log_prefix: str = ""
) -> Optional[Users]:
    log_t = log_prefix + "[{}]:".format(aget_object_of_log.__name__)

    try:
        user = await aget_object_or_404(model, pk=user_id)
        return user
    except Http404:
        log.warning("{} 'user' not exists!".format(log_t))
        return None
    except Exception as e:
        log.warning(log_t + " ERROR => {}".format(e.args if e.args else str(e)))
        return None


async def aget_object_from_allauth_or_log(
    index: int, log_prefix: str = ""
) -> Optional[AlluathEmailConfirmation]:
    from allauth.account.models import EmailConfirmation

    log_t = log_prefix + "[{}]:".format(aget_object_from_allauth_or_log.__name__)
    try:
        user = await aget_object_or_404(EmailConfirmation, email_address_id=index)
        return user
    except Http404:
        log.warning("{} 'user' not exists!".format(log_t))
        return None
    except Exception as e:
        log.warning(log_t + " ERROR => {}".format(e.args if e.args else str(e)))
        return None
