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
                email="w.nipuna@ucsc.cmb.ac.lk",
            ),
        )
        result: Dict[str, Any] = response.json
        print(result)
