# persons/tasks/sub_tascs_celery/sub_task_get_send_letter.py:1

import logging

from celery import shared_task

from persons import EnuSubjectOfLetter

log = logging.getLogger(__name__)


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
def task_child_process_letter_Thanks_for_your_account(self, *args, **kwargs) -> bool:
    """
    This task is an alert for a user - "This Email address was entered into a form of registration. ..." and more.
    :param self:
    :param args: Contain the emails addresses for a mailing.
    :param kwargs: empty
    :return: bool
    """
    from django.core.mail import send_mail
    from django.template.loader import render_to_string

    from persons import EnumEmailLetter
    from project.settings_conf.settings_env import APP_DEFAULT_FROM_EMAIL, APP_NAME

    log_t = f"[{task_child_process_letter_Thanks_for_your_account.__name__}]:"
    recipient_list_: list[str] = []
    try:
        log.info(
            log_t
            + f"""\n
        # ============================================
        # LETTER FOR THE USER'S EMAIL
        # ============================================
        # args: {str(args)}
        """
        )
        # That is context to the body of letter
        text_context = render_to_string(EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value)
        # Theme/Subject to the letter
        subject_ = EnuSubjectOfLetter.SUB_TASK_GET_SEND_LETTER_0.value
        for one_list in args:
            for u in one_list:
                em = u.__getitem__("to_email")
                recipient_list_.append(em)

        if len(recipient_list_) > 0:
            send_mail(
                subject=subject_,
                message=text_context,
                recipient_list=recipient_list_,
                from_email=APP_DEFAULT_FROM_EMAIL,
            )
            return True
    except Exception as e:
        error_t = " ".join([log_t, f" TEXT_ERROR: {e.args[0] if e.args else str(e)}"])
        log.error(error_t)
        raise self.retry(exc=e, countdown=30)
    log.info(
        log_t
        + " The 'EnumEmailLetter.CONFIRM_EMAIL_Letter_0' was sent to the %s recipient(s)."
        + str(len(recipient_list_))
    )
    return False
