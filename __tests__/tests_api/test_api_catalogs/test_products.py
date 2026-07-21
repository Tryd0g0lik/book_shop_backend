# __tests__/tests_api/test_api_catalogs/test_products.py:1
import asyncio
import logging
import math
import os
from typing import Optional

import pytest
from aiohttp import ClientSession, FormData
from django.db.models import QuerySet
from django.test import override_settings
from rest_framework import status

from __tests__.fixtures.fixture_django2 import pytest_generate_tests
from project import BASE_DIR

# Will run the APP !!

log = logging.getLogger(__name__)
log.info("============= STARTING TESTS =============")


class TestApiCatalogsValid:
    PREFIX_LOG = "[TestApiCatalogsValid]"
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
        log.info("{} Got a group name: {}".format(log_t, str(group.name)))
        user.groups.add(group)
        role_queryset: QuerySet = user.groups.values_list("name", flat=True)
        assert role_queryset.count() == 1
        log.info(
            "{} Created user. User Index: {} email: {} role: {}".format(log_t, user.id, new_users_registration["email"],
                                                                        role_queryset.first()))
        log.info("{} User got a group.".format(log_t))
        return user

    @pytest.fixture()
    def fixture_reade_file(self, path_file: Optional[str] = None) -> bool:
        log_t = "{}[fixture_reade_file]:".format(self.PREFIX_LOG, )
        path_file = self.TEST_FILES[0].replace("\\", "/") if path_file is None else path_file
        log.info("{} Got a path_file: {}".format(log_t, str(path_file)))
        assert os.path.exists(path_file)
        log.info("{} Got a file to the 'path_file' path: {}".format(log_t, str(path_file)))
        return True

    # @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    @pytest.mark.django_db(transaction=True)
    async def test_file_send_to_user_email_valid(self, fixture_reade_file, fixture_create_user):
        from catalog.permissions.permissions_checker import PermissionsChecker
        group = await fixture_create_user.groups.afirst()
        assert group is not None and hasattr(group, "name"), "Check a user role "

        # ProductViewSet
        log_t = "{}[test_file_send_to_user_email_valid]:".format(self.PREFIX_LOG, )
        log.info("{} start test".format(log_t))
        assert fixture_create_user.is_active == True
        # ============================================
        # STARTING A SESSION
        # ============================================
        async with ClientSession() as session:
            session.headers["contant_type"] = "multipart/form-data"
            setattr(session, "user", fixture_create_user)
            setattr(session.user, "is_active", True)
            if group.name.lower() == "admin":
                setattr(session.user, "is_superuser", True)
            if group.name.lower() != "client":
                setattr(session.user, "is_staff", True)
            # ============================================
            # TEST PERMISSION
            # ============================================
            try:
                await asyncio.to_thread(lambda: PermissionsChecker.can_add_product(session.user))
            except Exception as e:
                log.error("{} Error => {}".format(log_t, e.args[0] if e.args else str(e)))
                raise e
            log.info("{} Got a request user: {}".format(log_t, str(session.user)))
            test_path = self.TEST_FILES[0][:]
            log.info("{} Got a test_path: {}".format(log_t, test_path.split("\\")[-1]))

            size_chunk = 100
            total_chunks = 0
            total_file = b""
            # ============================================
            # READING THE TEST FILE XLSX
            # ============================================
            with open(file=test_path, mode="r+", encoding="utf-8", errors="ignore") as f:
                total_file = f.read()
                # Getting of chunks
                SEEK_END = f.seek(0, os.SEEK_END)
                log.info("{} Got a SEEK_END: {}".format(log_t, SEEK_END))
                file_size = f.tell()
                log.info("{} Got a st_size: {}".format(log_t, file_size))
                total_chunks = float(file_size / 1024 / size_chunk)
            sent_size = 0
            log.info("{} Got a total_chunks: {}".format(log_t, math.ceil(total_chunks)))
            # ============================================
            # FILE IS SENDING THROUGH CHUNKS
            # ============================================
            for i in range(1, math.ceil(total_chunks)):
                chunk_of_file = total_file[sent_size:i * size_chunk]
                sent_size += i * size_chunk
                log.info("{} Got a chunk_of_file: {}".format(log_t, chunk_of_file))
                # ============================================
                # GETTING A FORM DATA FOR THE EVERYTHING CHUNK
                # ============================================
                form_data = FormData()

                # Add the additional fields to the request.POST
                form_data.add_field('file_name', str(test_path.split("\\")[-1]))
                form_data.add_field('total_chunks', str(total_chunks))
                form_data.add_field('chunk_index', str(i))
                # Add (below) the additional fields to the request.FILES
                form_data.add_field(
                    'file',  # name of variable
                    chunk_of_file,  # That contains data/chunks of file.
                    filename=str(test_path.split("\\")[-1]),  # THe file name
                )
                log.info("{} Got a form data: {}".format(log_t, str(form_data)))
                # ============================================
                # SEND REQUEST TO THE SERVER
                # ============================================
                async with session.post("http://127.0.0.1:8000/api/download/load/file/",
                                        data=form_data, ) as response:
                    log.info("{} Got a load the XLS file to the request HTTP: {}".format(log_t, str(response.__dict__)))
                    log.info("{} Response Statuce response content: {}".format(log_t, str(response.content)))
                    log.info("{} Response Statuce code: {}".format(log_t, str(response.status)))

                    # assert "недостаточно прав" not in str(response.data["detail"])
                    assert response.status == status.HTTP_200_OK
                    # log.info("{} Got a test request".format(log_t, client.request.user))
                    # product_model = await asyncio.to_thread(ProductModel.objects.all)
                    # count = await product_model.acount()
                    # log.info("{} COunt of the product models: {}".format(log_t, str(count)))
