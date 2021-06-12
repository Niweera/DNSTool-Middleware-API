from .controllers import RootEndPointController, ZonesController
from flask_restful import Api


def initialize_routes(api: Api) -> None:
    api.add_resource(RootEndPointController, "/")
    api.add_resource(ZonesController, "/zones/<query>")
