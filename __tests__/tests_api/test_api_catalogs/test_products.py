# __tests__/tests_api/test_api_catalogs/test_products.py:1
# Whis is a Valid test. Here is checking (only) a property of load file.
# This test contain user's permissions and the mocker!
# Here is we checking upload Excel file,
# Excel file: small size; and checking the roles and permissions of roles.
import asyncio
import json
import logging
import math
import os
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, TypedDict

import pytest
from django.apps import apps
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
from django.test import AsyncRequestFactory
from rest_framework import status
from rest_framework.response import Response
from yarl import URL

# THE LINE BELOW/under it ( this notification) NOT DELETE!!
from __tests__.fixtures.fixture_parametrize2 import pytest_generate_tests
from download.views.view_load_file import DownloadOfCatalogViewSet
from project import BASE_DIR
from utilities.middleware.functions_jwt_tokens import (
    get_tokens_for_user,
)

ReqDict = TypedDict("ReqDict", {"method": str, "url": URL|str, "headers": Optional[Dict[str, str]],"data": Optional[Dict[str, str|bytes|int]]})
log = logging.getLogger(__name__)
log.info("============= STARTING 'TestApiUploadFileValid' TESTS =============")

class EnumExpansion(Enum):
    """It is expansion of files."""
    XSL = ['.xls', "application/vnd.ms-excel"]
    XSLX = ['.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]


class TestApiUploadFileValid:
    PREFIX_LOG = "[TestApiUploadFileValid]"
    TEST_FILES = [os.path.join(BASE_DIR, "__tests__", "fixtures", "template_catalog.xls")]
    CHUNK_SIZE: int = 1024 * 1024

    @pytest.fixture()
    def fixture_create_user(self, transactional_db, new_users_registration):
        """here is we creating a User (From common usr's data) in database and
         transmit the user data to the next test method. """
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.core.management import call_command
        log_t = "{}[fixture_create_user]:".format(self.PREFIX_LOG, )
        # ============================================
        # Create a test's environment
        # ============================================
        call_command("user_groups_db")
        log.info("{} Fulling the name of groups/roles in database.".format(log_t))
        Users = get_user_model()

        # ============================================
        # FILLING USER DATA TO THE DATABASE
        # ============================================
        password: str = new_users_registration["password1"]
        category: str = new_users_registration["category"]
        del new_users_registration["password1"], new_users_registration["password2"], \
            new_users_registration["check_user"], new_users_registration["category"]
        new_users_registration["password"] = password
        user, _ = Users.objects.get_or_create(**new_users_registration)
        # --- user group/role/permissions
        # ============================================
        # ADD A USER's GROUP
        #  it is regulator of permissions/right
        # ============================================
        group_name = category.capitalize()
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        if created:
            log.info("{} Group '{}' created successfully!".format(log_t, group_name))
        else:
            log.info("{} Group {} already exists!".format(log_t, group_name))
        role_queryset: QuerySet = user.groups.values_list("name", flat=True)
        assert role_queryset.count() == 1
        log.info(
            "{} Created user. User Index: {} email: {} role: {}".format(log_t, user.id, new_users_registration["email"],
                                                                        role_queryset.first()))
        log.info("{} User got a group {}.".format(log_t, (user.groups.first()).name))
        yield user

    @pytest.fixture()
    def fixture_reade_file(self, path_file: Optional[str] = None) -> bool:
        log_t = "{}[fixture_reade_file]:".format(self.PREFIX_LOG, )
        path_file = self.TEST_FILES[0].replace("\\", "/") if path_file is None else path_file
        log.info("{} Got a path_file: {}".format(log_t, str(path_file)))
        assert os.path.exists(path_file)
        log.info("{} Got a file to the 'path_file' path: {}".format(log_t, str(path_file)))
        return True

    @pytest.fixture
    def fixture_session_of_user(self, fixture_create_user):
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
        if group.name.lower() == "admin":
            setattr(session.user, "is_staff", True)
            setattr(session.user, "is_superuser", True)
        elif group.name.lower() == "client":
            # setattr(session.user, "is_staff", False)
            setattr(session.user, "is_superuser", False)
        elif group.name.lower() != "client" and group.name.lower() != "base":
            setattr(session.user, "is_staff", True)
        # ============================================
        # GETTING USER TOKEN
        # ============================================
        base64_token = get_tokens_for_user(fixture_create_user)
        session.headers.update({"Authorization": "Bearer {}".format(base64_token)})
        yield session


    @pytest.fixture
    def fixture_clearner(self):
        log_t = "{}[fixture_clearner]:".format(self.PREFIX_LOG, )
        # UP
        async def clearner_documents():
            try:
                # ============================================
                # CLEARING THE DATABASE 1/2
                # ============================================
                path = Path(str(BASE_DIR).replace("\\", "/") + "/media" + "/documents")
                for file in path.iterdir(): file.unlink()
            except Exception as e:
                error_t = "{} ERROR => {}".format(log_t, list(e.args)[0] if e.args else str(e))
                log.error(error_t)
                return False, list(e.args)[0] if e.args else str(e)
        # DOWN
        async def clearner_database():
            # ============================================
            # CLEARING THE DATABASE 2/2
            # ============================================
            try:
                ProductModel = apps.get_model("catalog", "ProductModel")
                await ProductModel.objects.all().adelete()
                return True, "The 'ProductModel' database was cleared successfully."
            except Exception as e:
                error_t = "{} ERROR => {}".format(log_t, list(e.args)[0] if e.args else str(e))
                log.error(error_t)
                return False, list(e.args)[0] if e.args else str(e)

        return clearner_documents, clearner_database


    @pytest.mark.asyncio
    async def test_upload_small_file(self,fixture_clearner, fixture_session_of_user):
        """Test uploading empty file, the permissions does not matter."""
        log_t = "{}[test_upload_small_file]:".format(self.PREFIX_LOG, )
        log.info("{} start test".format(log_t))
        clearner_documents, clearner_database = fixture_clearner
        # ============================================
        # CLEARING THE DATABASE 1/2
        # ============================================
        await clearner_documents()
        empty_file = SimpleUploadedFile("empty.xlsx", b"dasdasdwqre 34242 rfasdfdsf", content_type=EnumExpansion.XSLX.value[1])
        kwargs = dict()
        kwargs.__setitem__("path", "http://127.0.0.1:8000/api/download/load/file/")
        kwargs.__setitem__("headers", fixture_session_of_user.headers)
        files: dict = {"file": empty_file,
                       "total_chunks": str(len(list(empty_file.chunks()))),
                       "chunk_size": str(empty_file.size),
                       "file_name": empty_file.name,
                       "chunk_index": str(0)}
        kwargs.__setitem__("content_type", "multipart/form-data")
        # ============================================
        # START THE HANDLER OF FILES
        # ============================================
        factory = AsyncRequestFactory()
        requests = factory.post(**kwargs)
        requests.user = fixture_session_of_user.user
        setattr(requests.user, "is_sent", True)
        setattr(requests.user, "is_verified", True)
        setattr(requests.user, "is_superuser", True)
        requests.session = {}
        requests.session.__setitem__("user_id", fixture_session_of_user.user.id)
        requests._request = requests
        requests.METHOD = "POST"
        requests.META = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/api/download/load/file/",
        }
        requests.data = files
        # ============================================
        # OPEN THE VIEW CLASS FOR TESTS
        # ============================================
        log.info("{} Before send to the API's handler DownloadOfCatalogViewSet".format(log_t))
        catalog_file = DownloadOfCatalogViewSet()
        try:
            response: Response = await catalog_file.create(requests)
            log.info("{} Got Response: {}".format(log_t, str(response.__dict__)[:50]))
            detail_dict = json.loads((response.content).decode())
            assert "File to small size" in detail_dict.get("detail")
            assert response.status_code == status.HTTP_400_BAD_REQUEST
        except Exception as e:
            raise e
        finally:
            # ============================================
            # CLEARING THE DATABASE 2/2
            # ============================================
            await clearner_database()
    @pytest.mark.asyncio
    async def test_permissions_upload_file(self,fixture_clearner,
                                           fixture_session_of_user, ):
        """
        This test for testing the upload of file (xls) and permissions where the upload allows to be:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"
        and not allows:
        - user.groups == "client"
        - user.groups == "Base"
        :param fixture_session_of_user: This is Nock of a session was created for before tests and it is using now.
        ````text
            class Session:
            def __init__(self, user):
                self.user = user
                self.headers = dict()
        ```
        :return: We get a status code: 200 or 201 or 400 or 403
        """
        log_t = "{}[test_permissions_upload_file]:".format(self.PREFIX_LOG, )
        log.info("{} start test".format(log_t))

        clearner_documents, clearner_database = fixture_clearner

        # ============================================
        # CLEARING THE DATABASE 1/2
        # ============================================
        await clearner_documents()
        # ============================================
        # START A NEW TEST
        # ============================================
        file_name = self.TEST_FILES[0].split("\\")[-1]
        total_chunks_size = 3
        file_line = ""
        test_response = None

        with open(self.TEST_FILES[0], "rb" ) as f:
            file_line = f.read()
            log.info("{} Got a file_line Type: {}".format(log_t, type(file_line)))

        for i in range(total_chunks_size):
            start: int = i * (math.floor(len(file_line) / total_chunks_size))

            end: int = (start + 1) * (
                math.floor(len(file_line) / total_chunks_size)) if i < total_chunks_size - 1 else len(file_line)

            kwargs = dict()
            kwargs.__setitem__("path", "http://127.0.0.1:8000/api/download/load/file/")
            kwargs.__setitem__("headers", fixture_session_of_user.headers)

            files: dict = {"file": file_line[start:end],
                           "total_chunks":str(total_chunks_size),
                           "chunk_size":str(len(file_line[start:end])),
                           "file_name":file_name,
                           "filename":file_name,
                           "chunk_index": str(i)}

            kwargs.__setitem__("content_type", "multipart/form-data")
            # ============================================
            # START THE HANDLER OF FILES
            # ============================================
            factory = AsyncRequestFactory()
            requests = factory.post(**kwargs)
            requests.user = fixture_session_of_user.user
            setattr(requests.user, "is_sent", True)
            setattr(requests.user, "is_verified", True)

            requests.data = files

            requests.session = {}
            requests.session.__setitem__("user_id", fixture_session_of_user.user.id)
            requests._request = requests
            requests.METHOD = "POST"
            requests.META = {
                'REQUEST_METHOD': 'POST',
                'PATH_INFO': '/api/download/load/file/',
            }
            log.debug("{} Got Requests: {}".format(log_t, str(requests.__dict__))[:50])
            # ============================================
            # OPEN THE VIEW CLASS FOR TESTS
            # ============================================
            view = DownloadOfCatalogViewSet()
            resp = await view.create(requests)
            test_response = resp
            log.debug("""
            # ============================================
            # User: {}
            # ============================================
            """.format(str(requests.user.__dict__)))
        # ============================================
        # CHECK A RESPONSE (STATUS CODE) AFTER THE UPLOAD
        # ============================================
        status_code =  status.HTTP_201_CREATED if fixture_session_of_user.user.is_staff \
            else  status.HTTP_403_FORBIDDEN
        response_status_code = test_response.status_code
        assert response_status_code == status_code, "Allows {} status code!".format(status_code)
        # ============================================
        # CLEARING THE DATABASE 2/2
        # ============================================
        await clearner_database()
        await asyncio.sleep(1)
