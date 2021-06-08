from .controllers import RootEndPointController
from flask_restful import Api


def initialize_routes(api: Api) -> None:
    api.add_resource(RootEndPointController, "/")
