from flask import request, Response
import json
from models import LoginSchema
from functools import wraps
from middleware.error_handling import write_log

validator_schemas = {"login": LoginSchema}


def get_validation_schema(schema_name):
    if schema_name in validator_schemas:
        return validator_schemas[schema_name]()
    else:
        return False


def validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        body = request.get_json()
        if body:
            if hasattr(func.__self__, "model"):
                validation_schema = get_validation_schema(func.__self__.model)
                if validation_schema:
                    errors = validation_schema.validate(body)
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
            return send_error("Null body", "Request body is required")
        return func(*args, **kwargs)

    return wrapper


def send_error(error, message, code=None):
    write_log("error", error)
    return Response(
        response=json.dumps({"message": message}),
        status=(400, code)[code is not None],
        mimetype="application/json",
    )
