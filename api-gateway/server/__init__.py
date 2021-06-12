from os.path import abspath, join, dirname, realpath
from flask import Flask
from flask_cors import CORS
from cache import initialize_cache
from compress import initialize_compress
from controllers import initialize_routes
from flask_restful import Api
from middleware.error_handling import errors
from server.logging import initialize_logs
from swagger import initialize_swagger
from config import Config


app: Flask = Flask(
    __name__,
    static_folder=abspath(join(dirname(dirname(realpath(__file__))), "static")),
    static_url_path="/static",
)
app.config.from_object(Config)


if __name__ != "__main__":
    initialize_logs(app)

cors: CORS = CORS(
    app,
    resources={r"/*": {"origins": ["*"]}},
)
api: Api = Api(app, errors=errors)


initialize_cache(app)
initialize_compress(app)
initialize_swagger(app)
initialize_routes(api)
