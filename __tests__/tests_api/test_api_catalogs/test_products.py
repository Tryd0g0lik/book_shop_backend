# __tests__/tests_api/test_api_catalogs/test_products.py:1
# Whis is a Valid test. Here is checking (only) a property of load file.
# This test does not contain user's permissions!
import io
import json
import logging
import os
from enum import Enum
from typing import Optional

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response

from __tests__.fixtures.fixture_parametrize2 import pytest_generate_tests
from download.views.view_load_file import DownloadOfCatalogViewSet
from project import BASE_DIR
from utilities.middleware.functions_jwt_tokens import (
    get_tokens_for_user,
)

log = logging.getLogger(__name__)
log.info("============= STARTING TESTS =============")
# parametrize_roles = [
#     ("admin", {"staff": True, "superadmin": True, },201, "Superadmin has rights for a load Excel"),
#     ("Moderator", {"staff": True, "superadmin": False,}, 201, "Moderator has rights for a load Excel"),
#     ("Manager", {"staff": True, "superadmin": False, }, 201, "Manager has rights for a load Excel"),
#     ("editor", {"staff": True, "superadmin": False, },201,  "Editor has rights for a load Excel"),
#     ("client", {"staff": False, "superadmin": False, },401, "Client does not have rights for a load Excel"),
# ]

class EnumExpansion(Enum):
    """It is expansion of files."""
    XSL = ['.xls', "application/vnd.ms-excel"]
    XSLX = ['.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]


class TestApiUploadFileValid:
    PREFIX_LOG = "[TestApiUploadFileValid]"
    TEST_FILES = [os.path.join(BASE_DIR, "__tests__", "fixtures", "template_catalog.xlsx")]
    CHUNK_SIZE: int = 1024 * 1024

    @pytest.fixture()
    def fixture_create_user(self, transactional_db, new_users_registration):
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
        user = Users.objects.create(**new_users_registration)
        # --- user group/role/permissions
        group = Group.objects.get(name=category.capitalize())
        log.info("{} Got a group name: {} User ID: {}".format(log_t, str(group.name), str(user.id)))
        user.groups.add(group)
        role_queryset: QuerySet = user.groups.values_list("name", flat=True)
        assert role_queryset.count() == 1
        log.info(
            "{} Created user. User Index: {} email: {} role: {}".format(log_t, user.id, new_users_registration["email"],
                                                                        role_queryset.first()))
        log.info("{} User got a group.".format(log_t))
        yield user
        # user.delete()


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
        assert group is not None and hasattr(group, "name"), "Check a user role "
        # ============================================
        # STARTING A MOCK/PSEUDO SESSION
        # ============================================
        class Session:
            def __init__(self, user):
                self.user = user
                self.headers = dict()

        session = Session(fixture_create_user)
        session.headers.update({"contant_type": "multipart/form-data"})

        setattr(session.user, "is_active", True)
        setattr(session.user, "is_sent", True)
        setattr(session.user, "is_verified", True)
        if group.name.lower() == "admin":
            setattr(session.user, "is_staff", True)
            setattr(session.user, "is_superuser", True)
        elif group.name.lower() == "client":
            setattr(session.user, "is_staff", False)
            setattr(session.user, "is_superuser", False)
        elif group.name.lower() != "client":
            setattr(session.user, "is_staff", True)
        # ============================================
        # GETTING USER TOKEN
        # ============================================
        base64_token = get_tokens_for_user(fixture_create_user)
        session.headers.update({"Authorization": "Bearer {}".format(base64_token)})
        yield session
    @pytest.fixture
    def fixture_form_data(self):
        # ============================================
        # FORM DATA
        # ============================================
        class FormData:
            def __init__(self, file_line: str,
                         total_chunks: str,
                         chunk_size: str,
                         file_name: str):
                self.file: str = file_line  # InMemoryUploadedFile
                self.total_chunks: str = total_chunks
                self.chunk_size: str = chunk_size
                self.file_name: str = file_name

            def get(self, key: str, default=None):
                # This should work like a dictionary's get method
                if hasattr(self, key):
                    return getattr(self, key)
                return default

            def __getitem__(self, key):
                # Support dictionary-like access
                if hasattr(self, key):
                    return getattr(self, key)
                raise KeyError(key)

            def __contains__(self, key):
                return hasattr(self, key)
        yield FormData

    @pytest.fixture
    def fixture_open_file(self):
        log_t = "{}[fixture_open_file]:".format(self.PREFIX_LOG, )

        def wraper( test_path: str, size_chunk: int):
            # ============================================
            # OPENING FILE
            # ============================================
            with open(file=test_path, mode="rb", ) as f:
                part_file_line = f.read(size_chunk)
                log.info(
                    "{} GotTYpe: {}, the total_file_line: {}".format(log_t, type(part_file_line), part_file_line[:50]))
                try:
                    # ============================================
                    # BUFFER
                    # ============================================
                    f = io.BytesIO(part_file_line)
                    files_line = InMemoryUploadedFile(
                        file=f,
                        field_name="file",
                        size=len(part_file_line),
                        name=str(test_path.split("\\")[-1]),
                        content_type=EnumExpansion.XSL.value[1] if test_path.endswith(EnumExpansion.XSL.value[0]) else
                        EnumExpansion.XSLX.value[1],
                        charset=None,
                    )
                    yield files_line
                    log.debug(
                        "{} GotTYpe: {}, the total_file_line: {} sent success!".format(log_t, type(part_file_line),
                                                                         part_file_line[:50]))
                except (FileNotFoundError, FileExistsError) as e:
                    error_t = "{} FileNotFoundError => {}", log_t, list(e.args)[0] if e.args else str(e)
                    log.error(error_t)
                    raise FileNotFoundError(error_t) from e
                except Exception as e:
                    error_t = "{} Error => {}", log_t, list(e.args)[0] if e.args else str(e)
                    log.error(error_t)
                    raise ValueError(error_t) from e

        return wraper
    @pytest.fixture
    def fixture_test_request(self, fixture_form_data):
        FormData = fixture_form_data
        class TestRequest:
            def __init__(self, user, data: dict = None, files: Optional[FormData] = None):
                self.POST = data
                self.FILES = files
                self.user = user
        return TestRequest
    # @pytest.mark.parametrize("role, basis_role, expect, descript", parametrize_roles)
    @pytest.mark.django_db()
    @pytest.mark.asyncio
    async def test_upload_file_valid(self, mocker, fixture_reade_file, fixture_form_data,
                                     fixture_open_file, fixture_session_of_user,
                                     fixture_test_request):
        global response, total_file_line, total_chunks
        FormData = fixture_form_data
        TestRequest = fixture_test_request
        # ============================================
        # MOCKERS
        # ============================================
        mocker.patch("wagtail.tasks.update_reference_index_task", return_value=lambda app_label, model_name, pk: None)
        mocker.patch("download.task_save_file.task_sub_process_data", return_value=lambda data, user_id: None)
        mock_saving_data = mocker.patch("download.task_save_file.__init__.task_saving_data_oFfile")
        mock_saving_data.return_value=lambda *args, **kwargs: tuple("Hallo!")
        # ---
        log_t = "{}[test_upload_file_valid]:".format(self.PREFIX_LOG, )
        log.info("{} start test".format(log_t))

        test_path = self.TEST_FILES[0][:]
        log.info("{} Got a test_path: {}".format(log_t, test_path.split("\\")[-1]))
        size_chunk = self.CHUNK_SIZE

        for files_line in fixture_open_file(test_path, size_chunk):
            # ============================================
            # GETTING A FORM DATA FOR THE EVERYTHING CHUNK
            # ============================================
            data = dict()
            data.__setitem__('file_name', str(test_path.split("\\")[-1]))
            data.__setitem__('total_chunks', str(len(list(files_line.chunks()))))
            log.debug("{} total_chunks: {}, ".format(log_t, data.get("total_chunks", "")))
            # ============================================
            # CHUNKS
            # ============================================
            for i, view in enumerate(files_line.chunks()):
                data.__setitem__('chunk_size', str(len(view)))
                data.__setitem__("chunk_index", str(i))
                # ============================================
                # FORM DATA
                # ============================================
                formdata = FormData(file_line=view, chunk_size=str(len(view)), total_chunks=str(data.get("total_chunks")), file_name=data.get("file_name"), )
                files_line.close()


                request = TestRequest(user=fixture_session_of_user.user, data={"files":formdata, **data}, files=formdata)
                catalog_file = DownloadOfCatalogViewSet()
                response = await catalog_file.create(request)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_upload_small_file(self, fixture_test_request,fixture_form_data, fixture_session_of_user):
        """Test uploading empty file"""
        log_t = "{}[test_upload_small_file]:".format(self.PREFIX_LOG, )
        global request
        log.info("{} start test".format(log_t))
        TestRequest = fixture_test_request
        FormData = fixture_form_data
        empty_file = SimpleUploadedFile("empty.xlsx", b"dasdasdwqre 34242 rfasdfdsf", content_type=EnumExpansion.XSLX.value[1])
        data = dict()
        for view in empty_file.chunks():
            data.__setitem__('total_chunks', str(len(list(empty_file.chunks()))))
            data.__setitem__('file_name', "empty.xlsx")
            formdata = FormData(file_line=view, chunk_size=str(len(view)),
                                total_chunks=data.get('total_chunks'), file_name=data.get("file_name"), )
            data.__setitem__('chunk_size', str(len(view)))
            request = TestRequest(user=fixture_session_of_user.user, data={"file": formdata, **data}, files=formdata)
            log.info("{} Before send to the API's handler DownloadOfCatalogViewSet".format(log_t))
            catalog_file = DownloadOfCatalogViewSet()
            response: Response = await catalog_file.create(request)
            log.debug("{} DEBUG Got response: {}".format(log_t, str(response.__class__.__dict__)))
            log.info("{} Got response: {}".format(log_t, str(response.__dict__)))

        log.debug("{} response.content: {}".format(log_t, str(response.content)))
        detail_dict = json.loads((response.content).decode())
        assert "File to small size" in detail_dict.get("detail")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
