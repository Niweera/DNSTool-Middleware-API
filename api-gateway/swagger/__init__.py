from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = "/docs"
API_URL = "/static/openapi.json"


SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "DNSTool-Middleware-API Docs"},
)


def init_swagger(app):
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
