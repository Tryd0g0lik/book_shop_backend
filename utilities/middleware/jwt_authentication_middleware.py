# utilities/middleware/jwt_authentication_middleware.py:1
import base64
import json
import logging

import jwt
from django.contrib.auth.middleware import AuthenticationMiddleware
from rest_framework_simplejwt.tokens import RefreshToken

from persons.apps import DEBUG
from utilities.remove import check_token_status, verify_token_signature

log = logging.getLogger(__name__)


class JWTAuthenticationMiddleware(AuthenticationMiddleware):
    PREFIX_LOG = "[JWTAuthenticationMiddleware]"

    def process_request(self, request):
        global user_token, token_dict, user_id
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

        from .functions_jwt_tokens import decode_tokens_from_base64, get_tokens_for_user

        super().process_request(request)
        log_t = "{}[{}]:".format(
            self.PREFIX_LOG,
            self.process_request.__name__,
        )
        log.warning("{} DEBUG Request: {}".format(log_t, str(request.__dict__)))
        try:
            if "Authorization" in list(request.headers):
                try:
                    user_tokens_b64 = request.headers["Authorization"].split("Bearer ")[
                        -1
                    ]
                    # ============================================
                    # THE TOKENS DECODER
                    # ============================================
                    user_token = decode_tokens_from_base64(user_tokens_b64)

                    log.info(
                        "{} decode_tokens_from_base64 Token: {}".format(
                            log_t, str(user_token)
                        )
                    )
                    token_dict = dict()
                    if "access" in user_token:
                        try:
                            # --- Old token
                            access_token = user_token.get("access")
                            # token_obj = AccessToken(access_token)
                            token_obj = jwt.decode(
                                access_token, options={"verify_signature": False}
                            )
                            token_dict.update({"access": token_obj})
                        except TokenError as e:
                            log.warning(
                                "{} TokenError: {}".format(
                                    log_t, list(e.args)[0] if len(e.args) else str(e)
                                )
                            )
                            # ============================================
                            # UPDATING OF TOKEN
                            # Refresh token
                            # ============================================
                            log.info(
                                "{} TokenError: {}".format(
                                    log_t, list(e.args)[0] if len(e.args) else str(e)
                                )
                            )
                            log.info("{} TokenError: {}".format(log_t, str(user_token)))
                            if "refresh" in list(user_token):
                                refresh_token = user_token.get("refresh")
                                token_obj = jwt.decode(
                                    refresh_token, options={"verify_signature": False}
                                )
                                # token_obj = RefreshToken(user_token)
                                token_dict.update({"refresh": token_obj})
                    elif "refresh" in user_token:
                        refresh_token = user_token.get("refresh")
                        # token_obj = RefreshToken(user_token)
                        token_obj = jwt.decode(
                            refresh_token, options={"verify_signature": False}
                        )
                        token_dict.update({"refresh": token_obj})
                    else:
                        raise ValueError("No valid token in Base64 data")
                except NameError as e:
                    error_t = "{} NameError: {}".format(
                        log_t, list(e.args)[0] if len(e.args) else str(e)
                    )
                    log.error(error_t)
                    raise NameError(error_t) from e
                except (
                    base64.binascii.Error,
                    json.JSONDecodeError,
                    AssertionError,
                    ValueError,
                ) as e:
                    log.error(
                        "{} (base64.binascii.Error,\
                    json.JSONDecodeError,\
                    AssertionError,\
                    ValueError): {}".format(
                            log_t, list(e.args)[0] if len(e.args) else str(e)
                        )
                    )
                except TokenError as e:
                    error_t = "{} TokenError: {}".format(
                        log_t, list(e.args)[0] if len(e.args) else str(e)
                    )
                    log.error(error_t)
                    raise TokenError(error_t) from e
                # ============================================
                # AUTH OF USER
                # ============================================
                token_values_list = list(token_dict.values())
                token_keys_list = list(token_dict.keys())
                if len(token_values_list) > 0:
                    user_token = token_values_list.pop()

                    if "refresh" in token_keys_list:
                        user_id = user_token.access_token.get("user_id")
                    else:
                        user_id = user_token.get("user_id")
                    if user_id:
                        Users = get_user_model()
                        try:
                            user = Users.objects.get(id=user_id)
                            setattr(request, "user", user)
                        except Users.DoesNotExist:
                            log.warning(
                                "{} User's ID: {} not found!".format(log_t, user_id)
                            )

        except InvalidToken as e:
            log.warning(
                "{} Invalid Token: {}".format(
                    log_t, list(e.args)[0] if len(e.args) else str(e)
                )
            )

        except IndexError as e:
            log.error(
                "{} IndexError => {}".format(
                    log_t, list(e.args)[0] if len(e.args) else str(e)
                )
            )
        except Exception as e:
            log.error(
                "{} Error => {}".format(
                    log_t, list(e.args)[0] if len(e.args) else str(e)
                )
            )
            raise e
        finally:
            if not request.user.is_anonymous:
                # ============================================
                # THE ASSIGNED OF DATA TO THE REQUEST.HEADERS
                # ============================================
                try:
                    user_tokens_b64 = get_tokens_for_user(request.user)
                    tokens_dict = decode_tokens_from_base64(user_tokens_b64)
                    if DEBUG:
                        # Lock in the body of console
                        check_token_status(tokens_dict["access"])
                        verify_token_signature(tokens_dict["access"])
                    setattr(
                        request.headers,
                        "Authorization",
                        "Bearer {}".format(user_tokens_b64),
                    )
                except Exception as e:
                    error_t = "{} Error => {}".format(
                        log_t, list(e.args)[0] if len(e.args) else str(e)
                    )
                    log.error(error_t)
                    raise ValueError(error_t)
