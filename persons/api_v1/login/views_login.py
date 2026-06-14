# persons/api_v1/login/views_login.py:1

import logging

from adrf.generics import GenericAPIView
from adrf.mixins import RetrieveModelMixin, UpdateModelMixin
from adrf.viewsets import ViewSet
from allauth.account.views import LoginView
from django.shortcuts import aget_object_or_404
from rest_framework import status, validators

# from persons.api_v1.login.serializers import LoginSerializer
from persons.interfaces import UsersPydantic
from persons.models import Users

log = logging.getLogger(__name__)


# class LoginViewSet(UpdateModelMixin, GenericAPIView):
#
#     queryset = Users.objects.all()
#     serializer_class = UsersPydantic
#     # serializer_class = LoginSerializer
#     async def update(self, request, *args, **kwargs):
#
#         return super().update(request, *args, **kwargs)
