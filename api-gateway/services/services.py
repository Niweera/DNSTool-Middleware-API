import json
from os.path import abspath, join, dirname, realpath
from typing import List, Union, Dict, Any
from firebase_admin.auth import EmailAlreadyExistsError
from flask import Response
from config.CustomTypes import ResourceType
from database import FirebaseAuth, FirebaseDB
from middleware.error_handling import (
    write_log,
    NotFoundError,
    UnauthorizedError,
    InternalServerError,
)
from middleware.validator import send_error
import re
from services.mail_service import MailService


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
            zone_file: str = abspath(
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
            full_name: str = request_body.get("full_name")
            email: str = request_body.get("email")
            organization: str = request_body.get("organization")
            profession: str = request_body.get("profession")
            reason: str = request_body.get("reason")
            password: str = request_body.get("password")

            self.firebase_auth.register_user(
                full_name, email, organization, profession, reason, password
            )
            MailService.send_welcome_email(email, full_name)
            return dict(message="User account registered successfully"), 200
        except EmailAlreadyExistsError:
            return send_error(
                "Email already exists",
                f"The user with the provided email already exists",
                400,
            )
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError

    @staticmethod
    def check_email_domain(
        request_body: Dict[str, Any]
    ) -> Union[ResourceType, Response]:
        try:
            email: str = request_body.get("email")
            return dict(message=f"[{email}] is valid and accepted."), 200
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError

    @staticmethod
    def get_gcp_zone(query: str) -> Union[ResourceType, Response]:
        try:
            zone_file: str = abspath(
                join(dirname(dirname(realpath(__file__))), "static", "gcp-zones.json")
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

    def create_scan(self, request_body, uid) -> Union[ResourceType, Response]:
        try:
            self.firebase_db.store_scan_record(request_body, uid)
            return dict(message="Scan has successfully recorded"), 200
        except Exception as e:
            write_log("error", e)
            raise InternalServerError
