from typing import Dict, Any
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from tests.test_firebaser import get_id_token


class TestZonesController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()
        self.uid = "UchQlgJb9ibBoV991fqtQ5ykfHz2"

    def test_get_zone(self) -> None:
        response: TestResponse = self.app.get(
            "/zones/us", headers=dict(Authorization=f"Bearer {get_id_token(self.uid)}")
        )
        result: Dict[str, Any] = response.json
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("data"), list)
        self.assertEqual(len(result.get("data")), 20)
