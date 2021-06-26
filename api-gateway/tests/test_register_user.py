from typing import Dict, Any
from unittest import TestCase
from database import FirebaseAuth, FirebaseDB
from server import app
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class TestRegistrationController(TestCase):
    def setUp(self) -> None:
        self.firebase_auth: FirebaseAuth = FirebaseAuth()
        self.firebase_db: FirebaseDB = FirebaseDB()
        self.app: FlaskClient = app.test_client()
        self.email = "w.nipuna@ciu.ac.ug"
        self.failing_email = "w.nipuna@ciu.ac.gq"

    def test_register_user(self) -> None:
        response: TestResponse = self.app.post(
            "/register",
            json=dict(
                full_name="Nipuna Weerasekara",
                email=self.email,
                organization="Niweera.inc",
                profession="Web Developer",
                reason="For education purposes",
                password="super-secret",
            ),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), str)
        self.assertEqual(code, 200)

        # TearDown Test
        uid = self.firebase_auth.test_get_uid(self.email)
        self.firebase_auth.test_delete_user(uid)
        self.firebase_db.test_delete_user_data(uid)
        # TearDown Test

    def test_fail_register_user(self) -> None:
        response: TestResponse = self.app.post(
            "/register",
            json=dict(
                full_name="Nipuna Weerasekara",
                email=self.failing_email,
                organization="Niweera.inc",
                profession="Web Developer",
                reason="For education purposes",
                password="super-secret",
            ),
        )
        result: Dict[str, Any] = response.json
        code: int = response.status_code
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get("message"), dict)
        self.assertIsInstance(result.get("message").get("_schema"), list)
        self.assertEqual(code, 400)
