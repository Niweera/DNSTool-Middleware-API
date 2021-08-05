import json
from os.path import abspath, join, dirname, realpath
from typing import Union
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from tests.test_firebaser import get_id_token


class TestServiceAccountController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()
        self.uid = "UchQlgJb9ibBoV991fqtQ5ykfHz2"
        self.scan_id = "1625850846648708"

    def test_get_service_account(self) -> None:
        response: TestResponse = self.app.get(
            "/service-account/" + self.scan_id,
            headers=dict(Authorization=f"Bearer {get_id_token(self.uid)}"),
        )
        result: Union[bytes, str] = response.data
        file_name_header = response.headers["Content-Disposition"]
        file_name = file_name_header.split("=")[1]
        service_account = json.loads(result.decode("utf-8"))
        service_account_path = abspath(
            join(dirname(realpath(__file__)), "cli_client", file_name)
        )
        with open(service_account_path, "w") as json_file:
            json.dump(service_account, json_file, indent=2)
        code: int = response.status_code
        self.assertIsInstance(result, bytes)
        self.assertEqual(code, 200)

    def test_get_id_token(self) -> None:
        print(get_id_token(self.uid))
