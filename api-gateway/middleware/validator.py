from typing import Dict, Any, Optional, Union
from flask import request, Response
import json
from models import UserSchema
from functools import wraps
from middleware.error_handling import write_log

validator_schemas: Dict[str, Any] = {"User": UserSchema}


def get_validation_schema(schema_name: str) -> Union[Any, bool]:
    """
    :param str schema_name: Schema name
    :return: schema object
    """
    if schema_name in validator_schemas:
        return validator_schemas[schema_name]()
    else:
        return False


def validator(func: Any) -> Any:
    """
    :param callable func: Inner function
    :return: callable
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Dict[str, str]) -> Optional[Response]:
        request_body: Optional[Any] = request.get_json()
        if request_body:
            if hasattr(func.__self__, "model"):
                validation_schema: Optional[str, bool] = get_validation_schema(
                    func.__self__.model
                )
                if validation_schema:
                    errors: Optional[str, None] = validation_schema.validate(
                        request_body
                    )
                    if errors:
                        return send_error(errors, errors)
                else:
                    return send_error(
                        f"Validator class [{func.__self__.model}] not found",
                        "Internal Server Error",
                    )
            else:
                return send_error("Validator model undefined", "Internal Server Error")
        else:
            return send_error("Request body is undefined", "Request body is required")
        return func(*args, request_body, **kwargs)

    return wrapper


def send_error(error: str, message: str, code: Optional[int] = None) -> Response:
    """
    :param str error: error message to be logged
    :param str message: error message to be returned to the client
    :param int code: http error code
    :return: flask.Response
    """
    write_log("error", error)
    return Response(
        response=json.dumps({"message": message}),
        status=(400, code)[code is not None],
        mimetype="application/json",
    )
