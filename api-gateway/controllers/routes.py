from .controllers import (
    RootEndPointController,
    ZonesController,
    RegistrationController,
    EmailDomainCheckController,
    GCPZonesController,
)
from flask_restful import Api


def initialize_routes(api: Api) -> None:
    api.add_resource(RootEndPointController, "/")
    api.add_resource(ZonesController, "/zones/<query>")
    api.add_resource(RegistrationController, "/register")
    api.add_resource(EmailDomainCheckController, "/check-email")
    api.add_resource(GCPZonesController, "/gcp-zones/<query>")
