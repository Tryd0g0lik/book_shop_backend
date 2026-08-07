# utilities/middleware/functions_jwt_tokens.py:1

import base64
import json

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user) -> str:
    """Coding the dictionary tokens to the base64 string"""
    if not user.is_active:
        raise AuthenticationFailed("User is not active")
    # Getting access & refresh tokens
    refresh = RefreshToken.for_user(user)
    tokens = {"refresh": str(refresh), "access": str(refresh.access_token)}
    json_str = json.dumps(tokens)  # str
    json_bytes = json_str.encode("utf-8")  # bytes
    base64_encoded = base64.b64encode(json_bytes)  # bytes
    base64_str = base64_encoded.decode("utf-8")  # str
    return base64_str


def decode_tokens_from_base64(base64_str: str) -> dict:
    """Decoding Base64 string to the dist of tokens"""
    base64_bytes = base64_str.encode("utf-8")
    json_bytes = base64.b64decode(base64_bytes)
    json_str = json_bytes.decode("utf-8")
    return json.loads(json_str)
