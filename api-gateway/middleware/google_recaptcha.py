from functools import wraps
from typing import Dict, Optional, Callable, Any, Union
from config import Config
from config.CustomTypes import ResourceType
from middleware.validator import send_error
from flask import request, Response
import requests


def google_recaptcha(func: Callable[..., ResourceType]):
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Dict[str, str]) -> Union[ResourceType, Response]:
        request_body: Optional[Any] = request.get_json()
        g_recaptcha_response: str = request_body.get("g_recaptcha_response")

        if g_recaptcha_response:
            response: Any = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data=dict(
                    secret=Config.GOOGLE_RECAPTCHA_SECRET_KEY,
                    response=g_recaptcha_response,
                    remoteip=request.remote_addr,
                ),
            )

            response_dict: Dict[str, Any] = response.json()
            if (
                response_dict.get("success")
                and response_dict.get("score") > Config.GOOGLE_RECAPTCHA_SCORE_THRESHOLD
            ):
                return func(*args, **kwargs)
            else:
                return send_error(
                    "reCAPTCHA score is lower",
                    "Google reCAPTCHA validation failed!",
                    400,
                )
        else:
            return send_error(
                "No Google reCAPTCHA token provided",
                "Google reCAPTCHA v3 token is missing",
                400,
            )

    return wrapper
