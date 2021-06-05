from functools import wraps
from flask import request
from database import FirebaseAuth
from middleware.validator import send_error


firebase_auth = FirebaseAuth()


def authenticate(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token:
            decoded_token = firebase_auth.check_id_token(token.split("Bearer ")[1])
            if bool(decoded_token):
                return fn(*args, **kwargs)
            else:
                return send_error(
                    "Invalid Firebase authentication token", "Unauthorized", 401
                )
        else:
            return send_error("No JWT provided", "Unauthorized", 401)

    return wrapper
