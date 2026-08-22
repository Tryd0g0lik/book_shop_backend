# __tests__/tests_api/fixture_sessions_of_users.py:1
import pytest
from django.db import connection

from utilities.middleware.functions_jwt_tokens import (
    get_tokens_for_user,
)

pytest_plugins = [
    "__tests__.tests_api.fixture_creater_users"
]
@pytest.fixture
def fixture_session_of_user(fixture_create_user):
    assert fixture_create_user.is_active == True
    group = fixture_create_user.groups.first()
    assert group.name is not None and isinstance(group.name, str), "Check a user role "
    # ============================================
    # STARTING A MOCK/PSEUDO SESSION
    # ============================================
    class Session:
        def __init__(self, user):
            self.user = user
            self.headers = dict()

    session = Session(fixture_create_user)
    session.headers.update({"Content-Type": "multipart/form-data"})

    setattr(session.user, "is_active", True)
    setattr(session.user, "is_sent", True)
    setattr(session.user, "is_verified", True)
    setattr(session.user, "authenticators", True)
    setattr(session.user, "authenticators", True)
    if group.name.lower() == "admin":
        setattr(session.user, "is_staff", True)
        setattr(session.user, "is_superuser", True)
    elif group.name.lower() == "client":
        setattr(session.user, "is_staff", False)
        setattr(session.user, "is_superuser", False)
    elif group.name.lower() != "client" and group.name.lower() != "base":
        setattr(session.user, "is_staff", True)
    # ============================================
    # GETTING USER TOKEN
    # ============================================
    base64_token = get_tokens_for_user(fixture_create_user)
    session.headers.update({"Authorization": "Bearer {}".format(base64_token)})
    yield session
    connection.close()
