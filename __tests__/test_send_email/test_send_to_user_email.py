"""
__tests__/test_send_email/test_send_to_user_email.py:1
This Postman is sending letter  when we are working with PostmanAdapter.send_email_to_user. It is a person and it hase
the property: 'is_authenticated' or/and 'not is_anonymouse'.

"""

import logging

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import (
    mock_database_get_user_model,
    mock_database_get_user_model_2,
)
from persons import EnumEmailLetter
from persons.adapters import PostmanAdapter

log = logging.getLogger(__name__)


class TestSendToUserEmail:

    def test_send_to_user_email_no_valid(self):
        """Send Email (to the database User), here is returning True or mistake/"""
        from persons.adapters import PersonServiceDatabaseAdapter

        database_service_ = PersonServiceDatabaseAdapter()
        result_bool = False
        try:
            result_bool = PostmanAdapter.send_email_to_user(
                database_service=database_service_,
                subject_="First Test letter by the CONFIRM_EMAIL_Letter_0 template ",
                message_=EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value,
                user_id_=None,
                user_email_=None,
            )
        except Exception as e:
            assert (
                "We do not have the valid data!" in e.args[0] if e.args else str(e)
            ), "We should have the PersonErrorImproperlyConfigured."
        assert result_bool is not True, "User's Email or user's index must not be None."

    def test_send_to_user_email(self, users_model_data, mock_database_get_user_model_2):
        """Here us need to check the user_id_, subject_, user_email_. These data are: 'Yes - They are called'"""
        from persons.adapters import PersonServiceDatabaseAdapter, PostmanAdapter

        database_service_ = PersonServiceDatabaseAdapter()
        mock_user = users_model_data
        mock_user_id = mock_user.get("id")
        log.info(f"\nMock user ID: {str(mock_user_id)}")
        if mock_user_id in [4, 5, 7, 8, 10]:
            mock_user_email = mock_user.get("email")
            log.info(f"""\n
                # ============================================
                # TEST test_send_to_user_email AFTER CONDITION THAT IS id  in [4, 5, 7, 8, 10]:
                # ============================================
                # mock_user.id: {str(mock_user_id)}
                # mock_user.email: {str(mock_user_email)}
                """)
            # The database and the < model >.email_user were mock.
            lock = PostmanAdapter.lock
            result_bool = PostmanAdapter.send_email_to_user(
                database_service=database_service_,
                subject_="First Test letter by the CONFIRM_EMAIL_Letter_0 template %s"
                % mock_user_email,
                message_=EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value,
                user_id_=mock_user_id,
                user_email_=mock_user_email,
            )
            assert result_bool is True, "Email should be sent successfully"
            email = mock_database_get_user_model_2.method_calls[0].kwargs.get("email")
            assert email is not None, "Email should be sent successfully from Mock"
            assert isinstance(email, str), "Type String"
            assert (
                email == mock_user_email
            ), "Email should be equal to the email from the entrypoint \
of  PostmanAdapter.send_email_to_user(..., ...., ...., < EMAIL > from Mock) "
            log.info(
                f"TEST DEBUG method_calls: {mock_database_get_user_model_2.method_calls[0].kwargs}"
            )
