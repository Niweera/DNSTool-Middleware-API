from werkzeug.exceptions import HTTPException
from flask import current_app as app


class InternalServerError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


class NotFoundError(HTTPException):
    pass


errors = {
    "InternalServerError": {"message": "Internal Server Error", "status": 500},
    "UnauthorizedError": {"message": "Unauthorized", "status": 401},
    "NotFoundError": {"message": "Not Found", "status": 404},
}


def write_log(log_level, message):
    if log_level == "error":
        app.logger.error(message)
    elif log_level == "warning":
        app.logger.warning(message)
    elif log_level == "info":
        app.logger.info(message)
