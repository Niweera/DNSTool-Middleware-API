from os.path import abspath, join, dirname, realpath
from typing import Any, Dict
import firebase_admin
from firebase_admin import credentials, auth, db
from os import getenv
from dotenv import load_dotenv
from firebase_admin.auth import UserRecord, EmailAlreadyExistsError
from firebase_admin.db import Reference
from middleware.error_handling import write_log, UnauthorizedError, InternalServerError

load_dotenv()

cred: Any = credentials.Certificate(
    abspath(
        join(dirname(dirname(realpath(__file__))), "config", getenv("FIREBASE_JSON"))
    )
)
firebase_admin.initialize_app(cred, {"databaseURL": getenv("FIREBASE_DATABASE_URL")})


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

    def test_delete_user_data(self, uid: str) -> None:
        try:
            self.root.child("users").child(uid).delete()
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
