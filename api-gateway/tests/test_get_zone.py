from typing import Dict, Any
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class TestZonesController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()

    def test_get_zone(self) -> None:
        response: TestResponse = self.app.get("/zones/com")
        result: Dict[str, Any] = response.json
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("data"), list)
        self.assertEqual(len(result.get("data")), 11)
