import io
import json
from os.path import abspath, join, dirname, realpath
from typing import List, Union, Dict, Any, Optional, Tuple
from firebase_admin.auth import EmailAlreadyExistsError
from flask import Response, send_file, stream_with_context
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
from services.auth_service import AuthService
from services.mail_service import MailService
from storer import Storer


class Service:
    def __init__(self) -> None:
        self.firebase_auth: FirebaseAuth = FirebaseAuth()
        self.firebase_db: FirebaseDB = FirebaseDB()
        self.storer: Storer = Storer()

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

    def create_scan(
        self, uid: str, request_body: Dict[str, Any]
    ) -> Union[ResourceType, Response]:
        try:
            return self.firebase_db.store_scan_record(uid, request_body)
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_scans(self, uid: str) -> Union[ResourceType, Response]:
        try:
            data: object = self.firebase_db.get_scan_records(uid)
            return dict(data=data), 200
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def update_scan(
        self, uid: str, request_body: Dict[str, Any], **kwargs: Dict[str, str]
    ) -> Union[ResourceType, Response]:
        try:
            state: str = request_body.get("state", "")
            id: str = kwargs.get("id", "")
            self.firebase_db.update_scan_record(id, state, uid)
            return dict(message=f"[{id}] state updated successfully"), 200
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def delete_scan(
        self, uid: str, **kwargs: Dict[str, str]
    ) -> Union[ResourceType, Response]:
        try:
            id: str = kwargs.get("id", "")
            self.firebase_db.delete_scan_record(id, uid)
            return dict(message=f"scan [{id}] deleted successfully"), 200
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_service_account(
        self, uid: str, **kwargs: Dict[str, str]
    ) -> Union[ResourceType, Response]:
        try:
            id: str = kwargs.get("id", "")
            current_scans: Optional[
                List[Tuple[Any, ...]]
            ] = self.firebase_db.get_current_scanning_combinations(id, uid)
            if not current_scans:
                send_error(
                    "Scan is deleted or suspended by the user",
                    "Scan is deleted or suspended",
                    404,
                )
            private_key, public_key = AuthService.generate_rsa_key_pair()
            private_key_id: str = AuthService.generate_private_key_id()
            self.firebase_db.store_public_key(id, uid, public_key, private_key_id)
            email: object = self.firebase_db.get_user_email(uid)
            service_account: Dict[str, str] = dict(
                type="service_account",
                project_id="DNS-TOOL",
                private_key_id=private_key_id,
                private_key=private_key.decode("utf-8"),
                client_email=email,
                client_id=uid,
                scan_id=id,
                scans=current_scans,
            )
            service_account_dump: str = json.dumps(
                service_account, indent=2, sort_keys=False
            )
            service_account_binary: bytes = service_account_dump.encode()
            service_account_file: io.BytesIO = io.BytesIO(service_account_binary)
            response: Response = send_file(
                service_account_file,
                mimetype="text/json",
                as_attachment=True,
                download_name=f"service_account_{id}.json",
            )
            response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
            return response
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def list_downloads(
        self, uid: str, claims: Dict[str, str]
    ) -> Union[ResourceType, Response]:
        try:
            scan_id: str = claims.get("sid")
            current_scans: Optional[
                List[Tuple[Any, ...]]
            ] = self.firebase_db.get_current_scanning_combinations(scan_id, uid)
            aggregated_file_paths: List[str] = list()
            for scan in current_scans:
                scan_file_paths: List[str] = self.storer.get_file_paths_for_scan(scan)
                aggregated_file_paths.extend(scan_file_paths)
            return (
                dict(file_paths=aggregated_file_paths),
                200,
            )
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def download(
        self, uid: str, claims: Dict[str, str], **kwargs: Dict[str, str]
    ) -> Union[ResourceType, Response]:
        try:
            path: str = kwargs.get("path", "")
            scan_id: str = claims.get("sid")
            current_scans: Optional[
                List[Tuple[Any, ...]]
            ] = self.firebase_db.get_current_scanning_combinations(scan_id, uid)
            path_split: List[str] = path.split("/")
            region: str = path_split[0]
            zone: str = path_split[1]
            replaced_path: str = "_".join(path_split)

            if not dict(region=region, zone=zone) in current_scans:
                raise UnauthorizedError

            return Response(
                stream_with_context(self.storer.download_file(path)),
                mimetype=self.storer.get_download_file_mime_type(path),
                headers={
                    "Content-Disposition": f"attachment; filename={replaced_path}"
                },
            )
        except Exception as e:
            write_log("error", e)
            raise InternalServerError
