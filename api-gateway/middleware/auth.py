from functools import wraps
from typing import Dict, Optional, Callable, Any
from config.CustomTypes import ResourceType
from database import FirebaseAuth
from middleware.validator import send_error
from flask import request, Response

firebase_auth: FirebaseAuth = FirebaseAuth()


def authenticate(fn: Callable[..., ResourceType]):
    @wraps(fn)
    def wrapper(
        *args: Any, **kwargs: Dict[str, str]
    ) -> Optional[Callable[..., ResourceType], Response]:
        token: str = request.headers.get("Authorization")
        if token:
            decoded_token: Optional[
                Dict[str, str], None
            ] = firebase_auth.check_id_token(token.split("Bearer ")[1])
            if bool(decoded_token):
                return fn(*args, **kwargs)
            else:
                return send_error(
                    "Invalid Firebase authentication token", "Unauthorized", 401
                )
        else:
            return send_error("No JWT provided", "Unauthorized", 401)

    return wrapper
