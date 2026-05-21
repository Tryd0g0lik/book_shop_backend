# __tests__/test_send_email/test_send_to_user_email.py:1

import logging
from typing import Optional
from unittest.mock import Mock

import pytest
from django.db.models.expressions import result

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import mock_database_get_user_model
from persons import EnumEmailLetter
from persons.adapters import PostmanAdapter

log = logging.getLogger(__name__)

class TestSendToUserEmail:

    def test_send_to_user_email(self,   mock_database_get_user_model):

        mock_user = mock_database_get_user_model

        # assert int(mock_user.email) in [4, 5, 7, 8, 10]
        if mock_user.id  in [4, 5, 7, 8, 10]:
            log.info(f"\n===================== Check ID == {mock_user.id} ============")
            log.info("item.id " + str(mock_user.id))
            result = PostmanAdapter.send_email_to_user(
                subject_="First Test letter by the CONFIRM_EMAIL_Letter_0 template %s" % mock_user.email,
                message_=EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value,
                user_id_=mock_user.id,
                user_email_=mock_user.email,
            )
            assert result is True, "Email should be sent successfully"
