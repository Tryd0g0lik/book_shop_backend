# persons/forms/verification_form.py:1
import json
import logging
import re
from typing import Optional

from allauth.account.forms import UserTokenForm

from persons.apps import cachemanager
from persons.exceptions.error_forms import ErrorCodeVerificationForm

log = logging.getLogger(__name__)


class UsersCheckCodeVerificationForm(UserTokenForm):
    """
    Here we get the code verification. We have sent this code to the user's email address for email configuration.
    """

    uidb36 = None

    def _get_user(self, code_token: str) -> dict:
        """
        This code look up to the cache server by the template key from the selection
            list 'EnumTemplatesKeysCache.USER_PENDING_LETTER.value'.
        Time live extending on 300000 milliseconds.
        :param str code_token:
        :return: VERIFICATION CODE or the mistake name 'ErrorCodeVerificationForm'.
        """
        from utilities import EnumTemplatesKeysCache

        # Get user from cash server
        log_t = f"[{self.__class__.__name__}][{self._get_user.__name__}]:"
        cache_key = EnumTemplatesKeysCache.USER_PENDING_LETTER.value % "*"
        collection_keys = []
        log.info(
            f"""{log_t}
        # ============================================
        # LOOK UP THE VERIFICATION CODE BY TOKEN
        # ============================================
        """
        )
        try:
            # BELOW WE GET A LIST KEYS OF CACHE
            result_bool = cachemanager.aget(
                key_pattern=cache_key, collection=collection_keys
            )
            if result_bool is not None and len(collection_keys) >= 1:
                promocodes = []
                for key_bytes in collection_keys:
                    key_str = key_bytes.decode()
                    cachemanager.aget(key=key_str, collection=promocodes)
                # BELOW WE GOT A LIST OF JSON BYTES
                for view_bytes in promocodes:
                    view_json: dict = json.loads(view_bytes.decode())
                    # BELOW WE GET VALUES & LOOK UP THE VERIFICATION TOKEN IN HIM
                    verification_code: Optional[str] = view_json.get(
                        "verification_code"
                    )
                    if (
                        verification_code is not None
                        and verification_code == code_token
                    ):
                        promocodes.clear()
                        k = re.sub(
                            r"[@.]+", "", (cache_key[:-1] + view_json.get("email"))
                        )
                        cachemanager.aget(key=k, collection=promocodes, ex=300000)
                        # THE CODE VERIFICATION WAS FOUND & THE USER JSON DATA WE RETURN

                        return view_json

            raise ErrorCodeVerificationForm("Code verification invalid.")
        except Exception as e:
            raise ErrorCodeVerificationForm(e.args[0] if e.args else str(e)) from e

    def clean(self) -> dict:
        """
        TODO: Checking logic
        :return:
        """
        cleaned_data = super().clean()
        code_token = cleaned_data.get("code_token")

        if not code_token:
            raise ErrorCodeVerificationForm("Code was not found")
        try:
            result_json: dict = self._get_user(code_token)
            return result_json
        except Exception as e:
            raise e
