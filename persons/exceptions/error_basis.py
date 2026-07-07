# persons/exceptions/error_basis.py
# from typing import Optional
#
# from django.core.exceptions import ImproperlyConfigured
#
#
# class PersonError(ImproperlyConfigured):
#     def __init__(self, log_message: Optional[str] = "We do not have the valid data!"):
#         self._log_message = log_message
#         message: str = f"[{self.__class__.__name__}]:"
#
#         if log_message:
#             message += f"\n{message}" + self._log_message
#         super().__init__(message)
#
#     @property
#     def _log_message(self):
#         return self.__message
#
#     @_log_message.setter
#     def _log_message(self, log_message: Optional[str] = None):
#         self.__message: Optional[str] = log_message
