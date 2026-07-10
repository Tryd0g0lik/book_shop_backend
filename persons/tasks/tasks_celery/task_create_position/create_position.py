# persons/tasks/tasks_celery/task_create_position/create_position.py:1
import asyncio
import logging

from allauth.account.models import EmailAddress, EmailConfirmation
from django.utils import timezone
from playwright.sync_api import expect
from wagtail.users.models import UserProfile

from persons.models import Users

log = logging.getLogger(__name__)


async def create_position_for_EmailConfiguration(*args, **kwargs):
    log_t = "[task_create_position_for_EmailConfiguration]:"

    one_email = list(args)[0]
    generate_login_code = list(args)[1]
    # --- Allauth
    email_address = await asyncio.to_thread(
        lambda: EmailAddress.objects.get(email=one_email)
    )
    email_conf = EmailConfirmation(
        created=timezone.now(),
        sent=timezone.now(),
        key=generate_login_code,
        email_address_id=email_address.id,
    )
    await email_conf.asave()
    try:
        user = await Users.objects.aget(email=one_email)
        await UserProfile.objects.aget(user_id=user.id)
    except UserProfile.DoesNotExist:
        await UserProfile.objects.acreate(
            user=user,
        )
    log.info(log_t + "# save a verification code")
