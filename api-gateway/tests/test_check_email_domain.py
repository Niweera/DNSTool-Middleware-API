from typing import Dict, Any
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class TestEmailDomainCheckController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()

    def test_check_email_domain(self) -> None:
        response: TestResponse = self.app.post(
            "/check-email",
            json=dict(
                email="w.nipuna@ciu.ac.ug",
            ),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), str)
        self.assertEqual(code, 200)

    def test_check_email_sub_domain(self) -> None:
        response: TestResponse = self.app.post(
            "/check-email",
            json=dict(
                email="w.nipuna@stu.ciu.ac.ug",
            ),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), str)
        self.assertEqual(code, 200)

    def test_invalid_check_email_domain(self) -> None:
        response: TestResponse = self.app.post(
            "/check-email",
            json=dict(
                email="w.nipuna@ciu.ac.gq",
            ),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), dict)
        self.assertIsInstance(result.get("message").get("_schema"), list)
        self.assertEqual(code, 400)
