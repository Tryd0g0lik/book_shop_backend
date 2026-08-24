# __tests__/tests_api/test_api_catalogs/test_one_image.py:1
import io
import json
import logging
import os
import threading
from datetime import datetime
from multiprocessing.context import AuthenticationError

import pytest
from django.apps import apps
from django.contrib.auth.models import AnonymousUser, Group
from django.test import AsyncRequestFactory
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.test import force_authenticate

# Getting parameters
from __tests__.fixtures.fixture_parametrize2 import pytest_generate_tests
from catalog.intarfaces import ProductModelType
from catalog.views_api import OneImageViewSet
from project import BASE_DIR

# ============================================
# GETTING MODELS - THE WORKS ENVIRONMENT
# ============================================
ProductModel: ProductModelType = apps.get_model("catalog", "ProductModel")
CollectionModel = apps.get_model("wagtailcore", "Collection")
ImageModel = apps.get_model("wagtailimages", "Image")
UserProfileManagerModel = apps.get_model("profiles", "UserProfileManagerModel")
AdminProfileModel = apps.get_model("profiles", "AdminProfileModel")
ClientProfileModel = apps.get_model("profiles", "ClientProfileModel")
EditorProfileModel = apps.get_model("profiles", "EditorProfileModel")
ManagerProfileModel = apps.get_model("profiles", "ManagerProfileModel")
ModeratorProfileModel = apps.get_model("profiles", "ModeratorProfileModel")
CategoryModel = apps.get_model("catalog", "CategoryModel")
BrandModel = apps.get_model("catalog", "BrandModel")
UserProfile = apps.get_model("wagtailusers", "UserProfile")
# Getting fixtures
pytest_plugins = [
    "__tests__.tests_api.fixture_sessions_of_users",
]
log = logging.getLogger(__name__)

class TestOneImage:
    """It is a valid test for the 'OneImageViewSet' class"""
    PREFIX_LOG = "[TestOneImage]"
    TEST_FILE = [os.path.join(BASE_DIR, "__tests__", "fixtures", "jwt_by_api_map.png")]
    @pytest.fixture
    def fixture_mistake_role(self):
        async def get_role(group: Group, user_profile_data: dict):
            profile_obj, profile_manager = None, None
            if "admin" in group.name:
                profile_obj = await AdminProfileModel.objects.acreate(**user_profile_data)
                profile_manager = await UserProfileManagerModel.objects.acreate(admin=profile_obj)
            elif "client" in group.name:
                profile_obj = await ClientProfileModel.objects.acreate(**user_profile_data)
                profile_manager = await UserProfileManagerModel.objects.acreate(client=profile_obj)
            elif "editor" in group.name:
                profile_obj = await EditorProfileModel.objects.acreate(**user_profile_data)
                profile_manager = await UserProfileManagerModel.objects.acreate(editor=profile_obj)
            elif "manager" in group.name:
                profile_obj = await ManagerProfileModel.objects.acreate(**user_profile_data)
                profile_manager = await UserProfileManagerModel.objects.acreate(manager=profile_obj)
            elif "moderator" in group.name:
                profile_obj = await ModeratorProfileModel.objects.acreate(**user_profile_data)
                profile_manager = await UserProfileManagerModel.objects.acreate(moderator=profile_obj)
            return profile_obj, profile_manager
        return get_role
    # @pytest.mark.asyncio
    async def test_create_one_image_valid(self, transactional_db, fixture_session_of_user, fixture_mistake_role):
        """
        Checking valid data.
        :param mocker:
        :param transactional_db:
        :param fixture_session_of_user:  psevdo user data/parameters
        :return:
        """
        from PIL import Image


        try:
            prefix_log = "{}[{}]".format(self.PREFIX_LOG, "[test_create_one_image_valid]: ")
            # ============================================
            # CREATING THE REQUEST DATA OF THE POST
            # ============================================
            kwargs = dict()
            kwargs.__setitem__("path", "http://127.0.0.1:8000/api/catalog/image/acreate/")
            kwargs.__setitem__("headers", fixture_session_of_user.headers)
            kwargs["headers"].__setitem__("HTTP_AUTHORIZATION", fixture_session_of_user.headers.get("Authorization"))
            # ============================================
            # GETTING THE TEST DATA OF USER
            # ============================================
            user_obj = fixture_session_of_user.user
            group, profile_obj, profile_manager, test_response, file_image_bytes = None, None, None, None, None
            # ============================================
            # CHECKING THE EXISTS USER's GROUP
            # ============================================
            # log.debug("DEBUG is_user_exists[0]: {} & type: {}".format(str(is_user_exists), type(is_user_exists)))

            group = await user_obj.groups.afirst()
            if group.name.lower() != "client":

                # ============================================
                # CREATING THE TEST WAGTAIL's obj of UserProfile
                # ============================================
                magic_mock = await UserProfile.objects.acreate(id=user_obj.id,
                                                               submitted_notifications=1,
                                                                approved_notifications=1,
                                                                rejected_notifications=1,
                                                                user=user_obj,
                                                                updated_comments_notifications=1,
                                                                dismissibles={}, theme="system",	density="default",
                                                                contrast="system", keyboard_shortcuts=1)
                # ============================================
                # CREATE A TEST DATA  of AdminProfileModel
                # ============================================
                user_profile_data = {
                    "language": "ru",
                    "time_zone": "Asia/Kranoyarsk",
                    "dashboard_preference":"{}",
                    "user": magic_mock,
                }
                # ============================================
                # CREATING DEPENDENT MODELS
                # ============================================
                profile_obj, profile_manager = await fixture_mistake_role(group, user_profile_data)

                category_obj = await CategoryModel.objects.acreate(name="Test_category_name {}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%ms")),)
                brand_obj = await BrandModel.objects.acreate(name="Test_brand_name {}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%ms")),)
                product_obj = await ProductModel.objects.acreate(
                    is_active=True,
                    name="Наушники WH-1000XM5", product_sku=3,	price=34990,
                    product_discount=0,
                    describe_preview="Шумоподавление премиум-класса	Беспроводные, до 30 ч работы, быстрая зарядка",
                    discount_percent=15,
                    stock_quantity=120,	attributes_additional={"\u0422\u0438\u043f": " \u043f\u043e\u043b\u043d\u043e\u0440\u0430\u0437\u043c\u0435\u0440\u043d\u044b\u0435",
                                                                  " Bluetooth": " 5.2"},
                    brand=brand_obj,
                    category=category_obj,
                    created_by=profile_manager,
                    updated_by=profile_manager
                )

                collection_obj = await CollectionModel.objects.acreate(path=1, depth=1, numchild=0, 	name="Root")
                # # ============================================
                # CREATING THE TEST REQUEST
                # ============================================
                factory = AsyncRequestFactory()

                # ============================================
                # OPEN FILE IMAGES
                # ============================================
                with open(self.TEST_FILE[0].replace("\\", "/"), "rb") as f:
                    file_image_bytes = f.read()

                # ============================================
                # CREATING THE METHOD POST
                # ============================================
                filename = self.TEST_FILE[0].rsplit("\\", maxsplit=1)[-1]
                request = factory.post(**kwargs)
                image = Image.open(io.BytesIO(file_image_bytes))
                width, height = image.size
                # ============================================
                # GETING DATA OF A PRODUCT PAGE
                # ============================================
                log.debug("{} DEBUG CollectionModel Id: {}".format(prefix_log, str(collection_obj.id)))
                image_obj = await ImageModel.objects.acreate(file="original_images/{}".format(filename),
                                                             width = width,
                                                             height =  height,
                                                             description = "File '{}' {}*{}".format(filename, width, height),
                                                             title = filename,
                                                             collection_id = collection_obj.id,
                                                             uploaded_by_user_id = fixture_session_of_user.user.id)
                log.debug(("{} DEBUG Got the Image ID: {}".format(prefix_log, image_obj.id)))

                request.session = {}
                request.authenticators = True
                request.successful_authenticator = True
                request.user = fixture_session_of_user.user
                request._request = request
                log.debug("{} DEBUG User: '{}'".format(prefix_log, str(fixture_session_of_user.user.__dict__)))
                request.METHOD = "POST"
                request.META = {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO":"/api/catalog/image/acreate/"
                }
                request.data = {"product_id": product_obj.id,
                                "image_id": image_obj.id,
                                "describe": "",
                                "title": "Test_title_{}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%ms")),
                                "x": 0,
                                "y": 0,
                                }

                requsest_data = request.data
                log.debug("{} DEBUG \n Requests DATA: \n {}  ".format(prefix_log, str(requsest_data)[:50], ))
                try:
                    # ============================================
                    # User Auth
                    # ============================================
                    thread_ = threading.Thread(target=lambda : force_authenticate(request, user=fixture_session_of_user.user))
                    thread_.start()
                    thread_.join()
                    # ============================================
                    # Create the OneImageViewSet model
                    # ============================================
                    view = OneImageViewSet()
                    view.action = 'create'
                    test_response = await view.acreate(request)
                    log.debug("{} DEBUG \n Content: \n {}  ".format(prefix_log, str(test_response.__class__), ))
                    log.debug("{} DEBUG \n R T: \n {}  ".format(prefix_log, str(test_response)[:50], ))
                    log.debug("{} DEBUG \n Response Type: \n {}  ".format(prefix_log, type(test_response), ))
                    log.debug("{} DEBUG \n Response: \n {}  ".format(prefix_log, str(test_response.__class__.__dict__),))

                except (NotAuthenticated, PermissionDenied, AuthenticationError) as e:
                    log.debug("{} DEBUG AuthenticationError => {}  ".format(prefix_log, str(e), ))

                status_code = status.HTTP_200_OK if fixture_session_of_user.user.is_staff \
                    else status.HTTP_403_FORBIDDEN
                try:
                    assert test_response.status_code == status_code
                    assert type(test_response.content) == bytes
                    content = json.loads(test_response.content.decode())
                    assert content.get("detail").get("title") == request.data.get("title")

                except Exception as e:

                    raise e
        finally:
            pass

    async def test_error_403(self, fixture_session_of_user):
        """Checking the 403 mistake"""
        # ============================================
        # GRATING A REQUEST
        # ============================================
        qwargs = {
            "path": "/api/catalog/image/acreate/",
            "headers": fixture_session_of_user.headers,
        }
        factory = AsyncRequestFactory()
        request = factory.post(**qwargs)
        request.session = {}
        request.user = AnonymousUser
        request._request = request
        request.METHOD = "POST",
        request.META = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO":"/api/catalog/image/acreate/"
        }
        # ============================================
        # STARTING A TEST
        # ============================================
        view = OneImageViewSet()
        view.action = "create"
        test_response = await view.acreate(request)

        assert test_response.status_code == 403

    async def test_error_400(self, transactional_db, fixture_session_of_user, fixture_mistake_role):
        """Checking the 400 mistake"""
        # ============================================
        # CREATING THE REQUEST DATA OF THE POST
        # ============================================
        kwargs = dict()
        kwargs.__setitem__("path", "http://127.0.0.1:8000/api/catalog/image/acreate/")
        kwargs.__setitem__("headers", fixture_session_of_user.headers)
        kwargs["headers"].__setitem__("HTTP_AUTHORIZATION", fixture_session_of_user.headers.get("Authorization"))
        # ============================================
        # GETTING THE TEST DATA OF USER
        # ============================================
        user_obj = fixture_session_of_user.user
        # ============================================
        # CHECKING THE EXISTS USER's GROUP
        # ============================================
        group = await user_obj.groups.afirst()
        if group.name.lower() != "client":
            # ============================================
            # CREATING THE TEST WAGTAIL's obj of UserProfile
            # ============================================
            magic_mock = await UserProfile.objects.acreate(id=user_obj.id,
                                                           submitted_notifications=1,
                                                           approved_notifications=1,
                                                           rejected_notifications=1,
                                                           user=user_obj,
                                                           updated_comments_notifications=1,
                                                           dismissibles={}, theme="system",	density="default",
                                                           contrast="system", keyboard_shortcuts=1)
            # ============================================
            # CREATE A TEST DATA  of AdminProfileModel
            # ============================================
            user_profile_data = {
                "language": "ru",
                "time_zone": "Asia/Kranoyarsk",
                "dashboard_preference":"{}",
                "user": magic_mock,
            }
            # ============================================
            # CREATING DEPENDENT MODELS
            # ============================================
            profile_obj, profile_manager = await fixture_mistake_role(group, user_profile_data)

            category_obj = await CategoryModel.objects.acreate(name="Test_category_name {}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%ms")),)
            brand_obj = await BrandModel.objects.acreate(name="Test_brand_name {}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%ms")),)
            product_obj = await ProductModel.objects.acreate(
                is_active=True,
                name="Наушники WH-1000XM5", product_sku=3,	price=34990,
                product_discount=0,
                describe_preview="Шумоподавление премиум-класса	Беспроводные, до 30 ч работы, быстрая зарядка",
                discount_percent=15,
                stock_quantity=120,	attributes_additional={"\u0422\u0438\u043f": " \u043f\u043e\u043b\u043d\u043e\u0440\u0430\u0437\u043c\u0435\u0440\u043d\u044b\u0435",
                                                              " Bluetooth": " 5.2"},
                brand=brand_obj,
                category=category_obj,
                created_by=profile_manager,
                updated_by=profile_manager
            )
            # # ============================================
            # CREATING THE TEST REQUEST
            # ============================================
            factory = AsyncRequestFactory()
            request = factory.post(**kwargs)

            request.session = {}
            request.authenticators = True
            request.successful_authenticator = True
            request.user = fixture_session_of_user.user
            request._request = request
            request.METHOD = "POST"
            request.META = {
                "REQUEST_METHOD": "POST",
                "PATH_INFO":"/api/catalog/image/acreate/"
            }
            # ============================================
            # MIKE MISTAKES
            # ============================================
            request.data = {"product_id": 17, # inserting error data
                            "image_id": 22, # ... error data
                            "describe": "",
                            "title": "Test_title_{}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%ms")),
                            "x": 0,
                            "y": 0,
                            }
            # ============================================
            # User Auth
            # ============================================
            thread_ = threading.Thread(target=lambda : force_authenticate(request, user=fixture_session_of_user.user))
            thread_.start()
            thread_.join()
            # ============================================
            # Create the OneImageViewSet model
            # ============================================
            view = OneImageViewSet()
            view.action = 'create'

            test_response = await view.acreate(request)
            assert test_response.status_code == 400
