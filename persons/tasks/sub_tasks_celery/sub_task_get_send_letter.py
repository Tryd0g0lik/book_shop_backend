# persons/tasks/sub_tascs_celery/sub_task_get_send_letter.py:1

import logging
from typing import Any, Mapping, Optional

from celery import shared_task
from django.template.loader import get_template

from persons import EnumEmailLetter

log = logging.getLogger(__name__)


def child_process_emailing(*args, **kwargs):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string

    from project.settings_conf.settings_env import APP_DEFAULT_FROM_EMAIL, APP_NAME

    log_t = f"[task_child_process_letter_thanks_for_your_account][{child_process_emailing.__name__}]:"
    log.info(
        f"""\n
    DEBUG BEGINNING child_process_emailing:
    # kwargs: {kwargs}

"""
    )
    subject_: str = kwargs.get("subject")
    text_context: str = kwargs.get("text_context")
    context_: Optional[Mapping[str, Any]] = kwargs.get("context")

    recipient_list_: list[str] = []

    log.info(
        log_t
        + f"""\n
        # ============================================
        # LETTER FOR THE USER'S EMAIL
        # ============================================
        # args: {str(args)}
        # kwargs: {str(kwargs)}
        # contextx_: {str(context_)}
        """
    )

    log.info(
        f"""\n
    {str(text_context)}
"""
    )
    # That is context to the body of letter
    text_context = render_to_string(template_name=text_context, context=context_)
    log.info(
        f"""\n
        # ============================================
        # render_to_string FOR THE USER'S LETTER
        # ============================================
        # text_context: {text_context}
    """
    )
    # Theme/Subject to the letter

    for one_list in args:
        log.info(
            f"""\n
            DEBUG AFTER GOT one_list
        """
        )
        for u in one_list:
            em = u.__getitem__("email")
            recipient_list_.append(em)
    log.info(
        f"""\n
    DEBUG BEFORE SEND LETTER send_mail
"""
    )
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
