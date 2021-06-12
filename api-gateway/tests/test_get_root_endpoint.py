from typing import Dict
from unittest import TestCase
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from server import app


class TestRootEndPointController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()

    def test_get_root_endpoint(self) -> None:
        response: TestResponse = self.app.get("/")
        result: Dict[str, str] = response.json
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), str)
