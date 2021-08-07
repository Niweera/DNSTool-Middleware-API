import json
from datetime import datetime, timedelta
from os.path import abspath, join, dirname, realpath
from typing import Dict, List, Union, Any
import jwt
import requests
from flask import Response
from flask.testing import FlaskClient
from server import app
from werkzeug.test import TestResponse
from firebase_admin import credentials, auth
from os import getenv
import firebase_admin
from dotenv import load_dotenv

load_dotenv()

cred: Any = credentials.Certificate(
    abspath(
        join(
            dirname(dirname(dirname(realpath(__file__)))),
            "config",
            getenv("FIREBASE_JSON"),
        )
    )
)
firebase_admin.initialize_app(cred, name="CLI_APP")


class CLI:
    def __init__(self):
        service_account_file = abspath(
            join(dirname(realpath(__file__)), "service_account_1625850846648708.json")
        )
        with open(
            file=service_account_file, mode="r", encoding="utf-8"
        ) as service_account_json:
            service_account: Dict[str, Union[str, List[Dict[str, str]]]] = json.load(
                service_account_json
            )
            self.private_key_id: str = service_account.get("private_key_id")
            self.private_key: str = service_account.get("private_key")
            self.client_email: str = service_account.get("client_email")
            self.client_id: str = service_account.get("client_id")
            self.scan_id: str = service_account.get("scan_id")
            self.scans: List[Dict[str, str]] = service_account.get("scans")
            self.project_id: str = service_account.get("project_id")
            self.app: FlaskClient = app.test_client()

    def _create_jwt_token(self) -> str:
        return jwt.encode(
            dict(
                sid=self.scan_id,
                sub=self.client_id,
                iat=datetime.utcnow(),
                iss=self.project_id,
                pid=self.private_key_id,
                exp=datetime.utcnow() + timedelta(hours=1),
            ),
            self.private_key.encode(),
            algorithm="RS256",
        )

    def _firebase_token(self) -> str:
        custom_token: str = auth.create_custom_token(
            self.client_id, developer_claims=dict(scan_id=self.scan_id)
        ).decode("utf-8")
        res: Response = requests.post(
            f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={getenv('FIREBASE_API_KEY')}",
            data=dict(token=custom_token, returnSecureToken=True),
        )
        return res.json().get("idToken")

    def send_mock_download_request(self):
        response: TestResponse = self.app.get(
            "/download",
            headers=dict(
                Authorization=f"Bearer {self._create_jwt_token()}",
            ),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        print(result)
        print(code)

    def get_jwt_token(self):
        return self._create_jwt_token()

    def mock_run(self):
        response: TestResponse = self.app.get(
            "/list-downloads",
            headers=dict(Authorization=f"Bearer {self.get_jwt_token()}"),
            query_string=dict(client_id=self.client_id, scan_id=self.scan_id),
        )
        result: Dict[str, List[str]] = response.json
        file_paths: List[str] = result.get("file_paths")
        for file_path in file_paths:
            response: TestResponse = self.app.get(
                "/download/" + file_path,
                headers=dict(Authorization=f"Bearer {self.get_jwt_token()}"),
                query_string=dict(client_id=self.client_id, scan_id=self.scan_id),
            )
            result: Union[bytes, str] = response.data
            file_name_header: str = response.headers["Content-Disposition"]
            file_name: str = file_name_header.split("=")[1]
            file_save_path = abspath(
                join(dirname(realpath(__file__)), "static", file_name)
            )
            with open(file_save_path, "wb") as file:
                file.write(result)
