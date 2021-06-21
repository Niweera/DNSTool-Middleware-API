from collections import Callable
from typing import List, Dict, Any
from config.CustomTypes import ResourceType
from middleware.validator import validator
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


class RegistrationController(Resource):
    method_decorators: Dict[str, List[Callable]] = dict(post=[validator])
    model: str = "User"

    def post(self, request_body: Dict[str, Any]) -> ResourceType:
        return service.register_user(request_body)


class EmailDomainCheckController(Resource):
    method_decorators: Dict[str, List[Callable]] = dict(post=[validator])
    model: str = "OrganizationEmail"

    def post(self, request_body: Dict[str, Any]) -> ResourceType:
        return service.check_email_domain(request_body)


class GCPZonesController(Resource):
    @cache.cached(timeout=1000)
    def get(self, query: str) -> ResourceType:
        return service.get_gcp_zone(query)
