from .controllers import RootEndPointController


def initialize_routes(api):
    api.add_resource(RootEndPointController, "/")
