from services import Service
from flask_restful import Resource


service = Service()


class RootEndPointController(Resource):
    def get(self):
        return service.get_root_endpoint()
