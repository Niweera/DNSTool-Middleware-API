import json
from os.path import abspath, join, dirname, realpath
from typing import List, Union
from flask import Response
from config.CustomTypes import ResourceType
from middleware.validator import send_error
import re


class Service:
    @staticmethod
    def get_root_endpoint() -> ResourceType:
        return dict(message="Root Endpoint Accessed"), 200

    @staticmethod
    def get_zone(query: str) -> Union[ResourceType, Response]:
        zone_file = abspath(
            join(dirname(dirname(realpath(__file__))), "static", "zones.json")
        )
        with open(file=zone_file, mode="r", encoding="utf-8") as zones_json:
            zones: List[str] = json.load(zones_json)
            if type(zones) != list or len(zones) == 0:
                return send_error("error", "error occurred!", 404)

            lower_query: str = query.lower()
            result: List[str] = [
                entry for entry in zones if re.search(lower_query, entry)
            ]
            return dict(data=result), 200
