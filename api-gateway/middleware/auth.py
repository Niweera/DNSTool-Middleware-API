from functools import wraps
from typing import Dict, Optional, Callable, Any, Union
from config.CustomTypes import ResourceType
from database import FirebaseAuth
from middleware.validator import send_error
from flask import request, Response

firebase_auth: FirebaseAuth = FirebaseAuth()


def authenticate(func: Callable[..., ResourceType]):
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Dict[str, str]) -> Union[ResourceType, Response]:
        try:
            token: str = request.headers.get("Authorization")
            if token:
                uid: Optional[Dict[str, str], None] = firebase_auth.check_id_token(
                    token.split("Bearer ")[1]
                )
                if bool(uid):
                    return func(*args, uid, **kwargs)
                else:
                    return send_error(
                        "Invalid Firebase authentication token", "Unauthorized", 401
                    )
            else:
                return send_error("No JWT provided", "Unauthorized", 401)
        except Exception as e:
            return send_error(str(e), "Unauthorized", 401)

    return wrapper


def authenticate_service_account(func: Callable[..., ResourceType]):
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Dict[str, str]) -> Union[ResourceType, Response]:
        try:
            user_id: str = request.args.get("client_id")
            scan_id: str = request.args.get("scan_id")
            authorization_header: str = request.headers.get("Authorization")
            if user_id and scan_id and authorization_header:
                uid, claims = firebase_auth.validate_jwt(
                    user_id,
                    scan_id,
                    authorization_header,
                )
                if bool(uid) and bool(claims):
                    return func(*args, uid, claims, **kwargs)
                else:
                    return send_error(
                        "Invalid Firebase authentication token or JWT authentication token",
                        "Unauthorized",
                        401,
                    )
            else:
                return send_error("No JWT provided", "Unauthorized", 401)
        except Exception as e:
            return send_error(str(e), "Unauthorized", 401)

    return wrapper
