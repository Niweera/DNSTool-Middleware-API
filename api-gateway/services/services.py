from config.CustomTypes import ResourceType


class Service:
    @staticmethod
    def get_root_endpoint() -> ResourceType:
        return dict(message="Root Endpoint Accessed"), 200
