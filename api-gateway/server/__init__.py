from flask import Flask
from flask_cors import CORS
from cache import initialize_cache
from controllers import initialize_routes
from flask_restful import Api
from middleware.error_handling import errors
from server.logging import init_logs
from swagger import init_swagger
from config import Config


app: Flask = Flask(__name__, static_folder="../static", static_url_path="/static")
app.config.from_object(Config)


if __name__ != "__main__":
    init_logs(app)

cors: CORS = CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:3000"]}},
)
api: Api = Api(app, errors=errors)


initialize_cache(app)
init_swagger(app)
initialize_routes(api)
