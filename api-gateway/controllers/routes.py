from .controllers import (
    RootEndPointController,
    ZonesController,
    RegistrationController,
    EmailDomainCheckController,
    GCPZonesController,
    ScansController,
    ScanController,
    ServiceAccountController,
    DownloadListController,
    DownloadController,
)
from flask_restful import Api


def initialize_routes(api: Api) -> None:
    api.add_resource(RootEndPointController, "/")
    api.add_resource(ZonesController, "/zones/<query>")
    api.add_resource(RegistrationController, "/register")
    api.add_resource(EmailDomainCheckController, "/check-email")
    api.add_resource(GCPZonesController, "/gcp-zones/<query>")
    api.add_resource(ScansController, "/scans")
    api.add_resource(ScanController, "/scans/<id>")
    api.add_resource(ServiceAccountController, "/service-account/<id>")
    api.add_resource(DownloadListController, "/list-downloads")
    api.add_resource(DownloadController, "/download/<path:path>")
