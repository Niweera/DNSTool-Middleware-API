from os.path import abspath, join, dirname, realpath
from typing import Any, Dict
import firebase_admin
from firebase_admin import credentials, auth
from os import getenv
from dotenv import load_dotenv
from middleware.error_handling import write_log, UnauthorizedError

load_dotenv()

cred: Any = credentials.Certificate(
    abspath(
        join(dirname(dirname(realpath(__file__))), "config", getenv("FIREBASE_JSON"))
    )
)
firebase_admin.initialize_app(cred, {"databaseURL": getenv("FIREBASE_DATABASE_URL")})


class FirebaseAuth:
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
