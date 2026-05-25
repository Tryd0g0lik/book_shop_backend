# persons/tasks/tasks_celery/task_user_registration.py:1


import logging

from celery import shared_task

from persons.adapters.person_service_adapter import PersonServiceAdapter


@shared_task(
    name="task_user_registration_in_database",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError),
    retry_backoff=True,
    max_retries=3,
    countdown=3,
    retry_backoff_max=30,
)
def task_user_registration_in_database(self, args, kwargs):
    """

    :param self:
    :param args:
    :param kwargs: This is data if the new user must be registration.
        Example```dict
        {'category': 'BASE',
        'check_user': True,
        'email': 'test@email.ry',
        'first_name': 'Sergey',
        'password1': 'Eo121GOeWU6zaZgL', 'password2': 'Eo121GOeWU6zaZgL',
        'username': 'Sergey'}
        ```
    :return:
    """
    try:
        # personservice = PersonServiceAdapter
        for k, v in kwargs.items():
            pass
    except Exception as e:
        logging.error(e)
        raise self.retry(axc=e)
