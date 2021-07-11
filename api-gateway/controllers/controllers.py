from collections import Callable
from typing import List, Dict, Any
from config.CustomTypes import ResourceType
from middleware.auth import authenticate
from middleware.google_recaptcha import google_recaptcha
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
    method_decorators: Dict[str, List[Callable]] = dict(
        post=[validator, google_recaptcha]
    )
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


class ScansController(Resource):
    method_decorators: Dict[str, List[Callable]] = dict(post=[validator, authenticate])
    model: str = "CreateScan"

    def post(self, uid: str, request_body: Dict[str, Any]) -> ResourceType:
        return service.create_scan(uid, request_body)

    @authenticate
    def get(self, uid: str) -> ResourceType:
        return service.get_scans(uid)


class ScanController(Resource):
    method_decorators: Dict[str, List[Callable]] = dict(patch=[validator, authenticate])
    model: str = "UpdateScan"

    def patch(
        self, uid: str, request_body: Dict[str, Any], **kwargs: Dict[str, str]
    ) -> ResourceType:
        return service.update_scan(uid, request_body, **kwargs)

    @authenticate
    def delete(self, uid: str, **kwargs: Dict[str, str]) -> ResourceType:
        return service.delete_scan(uid, **kwargs)
