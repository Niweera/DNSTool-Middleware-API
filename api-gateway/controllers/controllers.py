from config.CustomTypes import ResourceType
from services import Service
from flask_restful import Resource


service: Service = Service()


class RootEndPointController(Resource):
    def get(self) -> ResourceType:
        return service.get_root_endpoint()
