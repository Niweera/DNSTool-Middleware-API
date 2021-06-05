from unittest import TestCase
from server import app


class RootEndPointController(TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_get_root_endpoint(self):
        response = self.app.get("/")
        result = response.json
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), str)
