from typing import Dict, List
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from tests.cli_client import CLI


class TestDownloadListController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()
        self.uid: str = "UchQlgJb9ibBoV991fqtQ5ykfHz2"
        self.scan_id: str = "1625850846648708"
        self.cli: CLI = CLI()

    def test_list_downloads(self) -> None:
        response: TestResponse = self.app.get(
            "/list-downloads",
            headers=dict(Authorization=f"Bearer {self.cli.get_jwt_token()}"),
            query_string=dict(client_id=self.uid, scan_id=self.scan_id),
        )
        result: Dict[str, List[str]] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("file_paths"), list)
        self.assertEqual(
            result.get("file_paths"),
            [
                "us-east1-c/.com/20210729.txt",
                "us-east1-c/.com/20210730.txt",
                "us-east1-c/.com/20210731.txt",
            ],
        )
        self.assertEqual(code, 200)
