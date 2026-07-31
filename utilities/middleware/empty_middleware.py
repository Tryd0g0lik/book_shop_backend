# utilities/middleware/empty_middleware.py:1
from django.contrib.auth.middleware import AuthenticationMiddleware, MiddlewareMixin


class EmptyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """This is the simple empty page. It is for testing and mocking process"""
        pass
