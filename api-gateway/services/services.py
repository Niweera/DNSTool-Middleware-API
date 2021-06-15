import json
from os.path import abspath, join, dirname, realpath
from typing import List, Union, Dict, Any
from flask import Response
from config.CustomTypes import ResourceType
from database import FirebaseAuth, FirebaseDB
from middleware.error_handling import write_log, NotFoundError, UnauthorizedError
from middleware.validator import send_error
import re


class Service:
    def __init__(self) -> None:
        self.firebase_auth: FirebaseAuth = FirebaseAuth()
        self.firebase_db: FirebaseDB = FirebaseDB()

    @staticmethod
    def get_root_endpoint() -> ResourceType:
        return dict(message="Root Endpoint Accessed"), 200

    @staticmethod
    def get_zone(query: str) -> Union[ResourceType, Response]:
        try:
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
        except Exception as e:
            write_log("error", e)
            raise NotFoundError

    def register_user(
        self, request_body: Dict[str, Any]
    ) -> Union[ResourceType, Response]:
        try:
            full_name = request_body.get("full_name")
            email = request_body.get("email")
            organization = request_body.get("organization")
            profession = request_body.get("profession")
            reason = request_body.get("reason")
            password = request_body.get("password")

            self.firebase_auth.register_user(
                full_name, email, organization, profession, reason, password
            )
            return dict(message="User account registered successfully"), 200
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError
