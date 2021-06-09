from config.CustomTypes import ResourceType
from services import Service
from flask_restful import Resource
from cache import cache

service: Service = Service()


class RootEndPointController(Resource):
    @cache.cached(timeout=1000)
    def get(self) -> ResourceType:
        return service.get_root_endpoint()


class ZonesController(Resource):
    @cache.cached(timeout=1000)
    def get(self, query: str) -> ResourceType:
        return service.get_zone(query)
