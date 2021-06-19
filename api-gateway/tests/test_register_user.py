from typing import Dict, Any
from unittest import TestCase
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class TestRegistrationController(TestCase):
    def setUp(self) -> None:
        self.app: FlaskClient = app.test_client()

    def test_register_user(self) -> None:
        response: TestResponse = self.app.post(
            "/register",
            json=dict(
                full_name="Nipuna Weerasekara",
                email="w.nipuna@gmail.com",
                organization="Niweera.inc",
                profession="Web Developer",
                reason="For education purposes",
                password="super-secret",
            ),
        )
        result: Dict[str, Any] = response.json
        print(result)
