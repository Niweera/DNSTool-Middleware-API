from os.path import abspath, join, dirname, realpath
import firebase_admin
from firebase_admin import credentials, auth
from os import getenv
from dotenv import load_dotenv
from middleware.error_handling import write_log, UnauthorizedError

load_dotenv()

cred = credentials.Certificate(
    abspath(join(dirname(realpath(__file__)), getenv("FIREBASE_JSON")))
)
firebase_admin.initialize_app(cred, {"databaseURL": getenv("FIREBASE_DATABASE_URL")})


class FirebaseAuth:
    @staticmethod
    def check_id_token(id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            write_log("error", e)
            raise UnauthorizedError
