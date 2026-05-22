# __tests__/test_send_email/test_send_to_user_email.py:1

import logging
from typing import Optional

import pytest

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import mock_database_get_user_model
from persons import EnumEmailLetter
from persons.adapters import PostmanAdapter

log = logging.getLogger(__name__)

class TestSendToUserEmail:

    def test_send_to_user_email_no_valid(self):
        """Send Email (to the database User), here is returning True or mistake/"""
        result_bool = False
        try:
            result_bool = PostmanAdapter.send_email_to_user(
                subject_="First Test letter by the CONFIRM_EMAIL_Letter_0 template " ,
                message_=EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value,
                user_id_=None,
                user_email_=None,
            )
        except Exception as e:
            assert 'We do not have the valid data!' in e.args[0] if e.args else str(e), "We should have the PersonErrorImproperlyConfigured."
        assert result_bool is not True, "User's Email or user's index must not be None."




    def test_send_to_user_email(self,   mock_database_get_user_model):
        """HEre, us need a check what the user_id_, subject_, user_email_ data is: Yes - They are called"""
        from django.core import mail
        mock_user = mock_database_get_user_model

        if mock_user.id  in [4, 5, 7, 8, 10]:
            # The database and the < model >.email_user were mock.
            result_bool = PostmanAdapter.send_email_to_user(
                subject_="First Test letter by the CONFIRM_EMAIL_Letter_0 template %s" % mock_user.email,
                message_=EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value,
                user_id_=mock_user.id,
                user_email_=mock_user.email,
            )
            assert result_bool is True, "Email should be sent successfully"
            sub = "First Test letter by the CONFIRM_EMAIL_Letter_0 template %s" % mock_user.email
            em = "host_test@email.ru"
            mock_user.email_user.assert_called_once_with(subject= sub,
                                                         message='account/email/email_confirmation_subject.txt',
                                                         from_email=em)
