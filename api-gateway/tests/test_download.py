from typing import Union
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from tests.cli_client import CLI


class TestDownloadController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()
        self.uid: str = "UchQlgJb9ibBoV991fqtQ5ykfHz2"
        self.scan_id: str = "1625850846648708"
        self.cli: CLI = CLI()
        self.file_path: str = "us-east1-c/.com/20210729.txt"

    def test_download(self) -> None:
        response: TestResponse = self.app.get(
            "/download/" + self.file_path,
            headers=dict(Authorization=f"Bearer {self.cli.get_jwt_token()}"),
            query_string=dict(client_id=self.uid, scan_id=self.scan_id),
        )
        result: Union[bytes, str] = response.data
        file_name_header: str = response.headers["Content-Disposition"]
        file_name: str = file_name_header.split("=")[1]
        file_data: str = result.decode("utf-8")
        code: int = response.status_code
        self.assertIsInstance(result, bytes)
        self.assertEqual(code, 200)
        self.assertEqual(file_name, "us-east1-c_.com_20210729.txt")
        self.assertEqual(file_data, "20210729.txt")
