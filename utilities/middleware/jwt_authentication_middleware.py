# utilities/middleware/jwt_authentication_middleware.py:1
import logging

from django.contrib.auth.middleware import AuthenticationMiddleware
from rest_framework_simplejwt.tokens import RefreshToken

from persons.apps import DEBUG
from utilities.remove import check_token_status, verify_token_signature

log = logging.getLogger(__name__)


class JWTAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from rest_framework_simplejwt.tokens import AccessToken

        from .functions_jwt_tokens import decode_tokens_from_base64, get_tokens_for_user

        super().process_request(request)
        log_t = "[{}][{}]:".format(
            JWTAuthenticationMiddleware.__class__.__name__,
            self.process_request.__name__,
        )
        if "Authorization" in list(request.headers.keys()):
            try:
                tokens = request.headers["Authorization"].split(" ")[1]
                # ============================================
                # THE TOKENS DECODER
                # ============================================
                token = decode_tokens_from_base64(tokens)
                token_dict = dict()
                if "access" in list(token.keys()):
                    try:
                        # --- Old token
                        token_obj = AccessToken(token["access"])
                        token_dict.update({"access": token_obj})
                    except TokenError as e:
                        log.warning(
                            "{} TokenError: {}".format(
                                log_t, e.args[0] if len(e.args) else str(e)
                            )
                        )
                        # ============================================
                        # UPDATING OF TOKEN
                        # Refresh token
                        # ============================================
                        if "refresh" in list(token.keys()):
                            token_obj = RefreshToken(token["refresh"])
                            token_dict.update({"refresh": token_obj})
                elif "refresh" in list(token.keys()):
                    token_obj = RefreshToken(token["refresh"])
                    token_dict.update({"refresh": token_obj})
                # ============================================
                # AUTH OF USER
                # ============================================
                token_values_list = list(token_dict.values())
                token_keys_list = list(token_dict.keys())
                if len(token_values_list) > 0:
                    token = token_values_list.pop()
                    user_id = None
                    if "refresh" in token_keys_list:
                        user_id = token.access_token.payload.get("user_id")
                    else:
                        user_id = token.payload.get("user_id")
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
                        log_t, e.args[0] if len(e.args) else str(e)
                    )
                )

            except IndexError as e:
                log.error(
                    "{} IndexError => {}".format(
                        log_t, e.args[0] if len(e.args) else str(e)
                    )
                )
            finally:
                if not request.user.is_anonymous:
                    # ============================================
                    # THE ASSIGNED OF DATA TO THE REQUEST.HEADERS
                    # ============================================
                    try:
                        tokens = get_tokens_for_user(request.user)
                        tokens_dict = decode_tokens_from_base64(tokens)
                        if DEBUG:
                            # Lock in the body of console
                            check_token_status(tokens_dict["access"])
                            verify_token_signature(tokens_dict["access"])
                        setattr(
                            request.headers, "Authorization", "Bearer {}".format(tokens)
                        )
                    except Exception as e:
                        log.error(
                            "{} Error => {}".format(
                                log_t, e.args[0] if len(e.args) else str(e)
                            )
                        )
