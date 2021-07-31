import itertools
from os.path import abspath, join, dirname, realpath
from typing import Any, Dict, List, Union, Tuple, Optional
import firebase_admin
import jwt
from firebase_admin import credentials, auth, db
from firebase_admin.auth import UserRecord, EmailAlreadyExistsError
from firebase_admin.db import Reference
from flask import Response
from config import Config
from config.CustomTypes import ResourceType
from middleware.error_handling import write_log, UnauthorizedError, InternalServerError
from datetime import datetime
from itertools import chain
from middleware.validator import send_error


cred: Any = credentials.Certificate(
    abspath(join(dirname(dirname(realpath(__file__))), "config", Config.FIREBASE_JSON))
)
firebase_admin.initialize_app(cred, {"databaseURL": Config.FIREBASE_DATABASE_URL})


class FirebaseDB:
    def __init__(self) -> None:
        self.root: Reference = db.reference()

    def create_user_account(
        self,
        uid: str,
        full_name: str,
        email: str,
        organization: str,
        profession: str,
        reason: str,
    ) -> None:
        try:
            self.root.child("users").child(uid).set(
                dict(
                    full_name=full_name,
                    email=email,
                    organization=organization,
                    profession=profession,
                    reason=reason,
                )
            )
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError

    def store_scan_record(
        self, uid: str, request_body: Dict[str, List[str]]
    ) -> Union[ResourceType, Response]:
        try:
            zones: List[str] = list(set(request_body.get("zones")))
            regions: List[str] = list(set(request_body.get("regions")))
            input_scanning_combinations: List[Tuple[str, str]] = list(
                itertools.product(zones, regions)
            )
            scans: object = self.get_scan_records(uid)
            if not bool(scans):
                scans: Dict[str, Dict[str, Any]] = dict()
            current_zones_list: List[str] = [scans[id]["zones"] for id in scans]
            current_zones: List[str] = list(set(chain(*current_zones_list)))
            current_regions_list: List[str] = [scans[id]["regions"] for id in scans]
            current_regions: List[str] = list(set(chain(*current_regions_list)))
            current_scanning_combinations: List[Tuple[Any, ...]] = list(
                itertools.product(current_zones, current_regions)
            )
            available_scans: List[Tuple[Any, ...]] = list(
                set(input_scanning_combinations).difference(
                    set(current_scanning_combinations)
                )
            )
            if len(available_scans) > 0:
                available_zones, available_regions = zip(*available_scans)
            else:
                available_zones, available_regions = list(), list()

            if len(available_zones) > 0 and len(available_regions) > 0:
                self.root.child("users").child(uid).child("scans").child(
                    str(datetime.now().timestamp()).replace(".", "")
                ).set(
                    dict(
                        zones=list(set(available_zones)),
                        regions=list(set(available_regions)),
                        state="active",
                    )
                )
                return dict(message="Scan has successfully recorded"), 200
            else:
                return send_error(
                    "no new scannable zones, regions to set",
                    "The zones and regions you set are already scanning",
                )
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_scan_records(self, uid: str) -> object:
        try:
            scans: object = self.root.child("users").child(uid).child("scans").get()
            return scans
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def test_delete_user_data(self, uid: str) -> None:
        try:
            self.root.child("users").child(uid).delete()
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def update_scan_record(self, id: str, state: str, uid: str) -> None:
        try:
            self.root.child("users").child(uid).child("scans").child(id).child(
                "state"
            ).set(state)
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def delete_scan_record(self, id: str, uid: str) -> None:
        try:
            self.root.child("users").child(uid).child("scans").child(id).delete()
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_current_scanning_combinations(
        self, id: str, uid: str
    ) -> Optional[List[Dict[str, str]]]:
        try:
            scan: object = (
                self.root.child("users").child(uid).child("scans").child(id).get()
            )
            state: str = scan["state"]

            if state != "active":
                return None

            current_scanning_combinations: List[Tuple[Any, ...]] = list(
                itertools.product(scan["regions"], scan["zones"])
            )
            current_scans: List[Dict[str, str]] = [
                dict(region=region, zone=zone)
                for region, zone in current_scanning_combinations
            ]
            return current_scans
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def store_public_key(
        self, id: str, uid: str, public_key: bytes, private_key_id: str
    ) -> None:
        try:
            self.root.child("public_keys").child(uid).child(id).set(
                dict(
                    public_key=public_key.decode("utf-8"),
                    private_key_id=private_key_id,
                )
            )
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_user_email(self, uid: str) -> object:
        try:
            email: object = self.root.child("users").child(uid).child("email").get()
            return email
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_public_key(self, uid: str, scan_id: str) -> str:
        try:
            return str(
                self.root.child("public_keys")
                .child(uid)
                .child(scan_id)
                .child("public_key")
                .get()
            )
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_private_key_id(self, uid: str, scan_id: str) -> str:
        try:
            return str(
                self.root.child("public_keys")
                .child(uid)
                .child(scan_id)
                .child("private_key_id")
                .get()
            )
        except Exception as e:
            write_log("error", e)
            raise InternalServerError


class FirebaseAuth:
    def __init__(self) -> None:
        self.firebase_db: FirebaseDB = FirebaseDB()

    @staticmethod
    def check_id_token(id_token: str) -> str:
        try:
            decoded_token: Dict[str, str] = auth.verify_id_token(id_token)
            if bool(decoded_token):
                return decoded_token.get("user_id")
            else:
                raise UnauthorizedError
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError

    def validate_jwt(
        self, firebase_token_header: str, authorization_header: str
    ) -> Tuple[str, Dict[str, str]]:
        try:
            firebase_token: str = firebase_token_header.split("Bearer ")[1]
            authorization_token: str = authorization_header.split("Bearer ")[1]
            decoded_firebase_token: Dict[str, str] = auth.verify_id_token(
                firebase_token
            )

            if not bool(decoded_firebase_token):
                raise UnauthorizedError

            uid: str = decoded_firebase_token.get("user_id")
            scan_id: str = decoded_firebase_token.get("scan_id")

            if not (bool(uid) and bool(scan_id)):
                raise UnauthorizedError

            public_key: str = self.firebase_db.get_public_key(uid, scan_id)

            if not bool(public_key):
                raise UnauthorizedError

            decoded_authorization_claims: Dict[str, str] = jwt.decode(
                authorization_token,
                public_key.encode(),
                algorithms=["RS256"],
                options={"require": ["sid", "sub", "iat", "iss", "pid", "exp"]},
            )

            private_key_id_from_claims: str = decoded_authorization_claims.get("pid")
            scan_id_from_claims: str = decoded_authorization_claims.get("sid")
            uid_from_claims: str = decoded_authorization_claims.get("sub")
            recorded_private_key_id: str = self.firebase_db.get_private_key_id(
                uid, scan_id
            )

            if private_key_id_from_claims != recorded_private_key_id:
                raise UnauthorizedError

            if scan_id_from_claims != scan_id:
                raise UnauthorizedError

            if uid_from_claims != uid:
                raise UnauthorizedError

            return uid, decoded_authorization_claims
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError

    def register_user(
        self,
        full_name: str,
        email: str,
        organization: str,
        profession: str,
        reason: str,
        password: str,
    ) -> None:
        try:
            user_record: UserRecord = auth.create_user(
                email=email,
                email_verified=False,
                password=password,
                display_name=full_name,
            )
            self.firebase_db.create_user_account(
                user_record.uid, full_name, email, organization, profession, reason
            )
        except EmailAlreadyExistsError:
            raise EmailAlreadyExistsError(None, None, None)
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError

    @staticmethod
    def test_get_uid(email: str) -> str:
        try:
            return auth.get_user_by_email(email).uid
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    @staticmethod
    def test_delete_user(uid: str) -> str:
        try:
            return auth.delete_user(uid)
        except Exception as e:
            write_log("error", e)
            raise InternalServerError
