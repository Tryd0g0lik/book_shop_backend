# persons/tasks/sub_tascs_celery/sub_task_get_send_letter.py:1
import json
import logging
from typing import Any, Mapping, Optional

from celery import shared_task

log = logging.getLogger(__name__)


def child_process_emailing(*args, **kwargs):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string

    from persons.models import Users
    from project.settings_conf.settings_env import APP_DEFAULT_FROM_EMAIL

    log.info(
        f"""\n
    # ============================================
    # DEBUG child_process_emailing
    # args: {args}
    # kwargs: {kwargs}
    # subject_: str = {kwargs.get("subject")}
    #     text_context: str = {kwargs.get("text_context")}
    #     context_: Optional[Mapping[str, Any]] = {kwargs.get("context")}
    #     context_['user'] = {json.loads((kwargs.get("context"))['user'])}
    # ============================================
"""
    )
    subject_: str = kwargs.get("subject")
    text_context: str = kwargs.get("text_context")
    context_: Optional[Mapping[str, Any]] = kwargs.get("context")
    context_["user"] = json.loads(context_["user"])
    recipient_list_: list[str] = []
    # That is context to the body of letter
    text_context = render_to_string(template_name=text_context, context=context_)
    for one_list in args:
        for u in one_list:
            em = u.__getitem__("email")
            recipient_list_.append(em)

    if len(recipient_list_) > 0:
        send_mail(
            subject=subject_,
            message=text_context,
            recipient_list=recipient_list_,
            from_email=APP_DEFAULT_FROM_EMAIL,
        )
        return True


# ============================================
# SUB PROCES FOR THE SENDING OF LETTER
# ============================================
@shared_task(
    name="sub_task_get_send_letter",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError),
    retry_backoff=True,
    max_retries=3,
    retry_backoff_max=30,
)
def task_child_process_letter_thanks_for_your_account(self, *args, **kwargs) -> bool:
    """
    This task is an alert for a user - "This Email address was entered into a form of registration. ..." and more.
    :param self:
    :param args: Contain the emails addresses for a mailing.
    :param kwargs: empty
    :return: bool
    """

    log_t = f"[{task_child_process_letter_thanks_for_your_account.__name__}]:"
    try:
        child_process_emailing(*args, **kwargs)
        return True
    except Exception as e:
        error_t = " ".join([log_t, f" TEXT_ERROR: {e.args[0] if e.args else str(e)}"])
        log.error(error_t)
        raise self.retry(exc=e, countdown=30)
