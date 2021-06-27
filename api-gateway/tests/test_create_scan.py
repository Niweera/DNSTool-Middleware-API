from typing import Dict, Any
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from tests.test_firebaser import get_id_token


class TestCreateScanController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()
        self.uid = "UchQlgJb9ibBoV991fqtQ5ykfHz2"

    def test_create_scan(self) -> None:
        response: TestResponse = self.app.post(
            "/scans",
            json=dict(
                zones=[".com", ".lk"],
                regions=["us-east1-b", "us-east1-c"],
            ),
            headers=dict(Authorization=f"Bearer {get_id_token(self.uid)}"),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), str)
        self.assertEqual(result.get("message"), "Scan has successfully recorded")
        self.assertEqual(code, 200)
