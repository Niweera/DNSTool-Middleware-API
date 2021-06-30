from os import getenv
from typing import Any
import firebase_admin
from firebase_admin import credentials, auth
from os.path import abspath, join, dirname, realpath
import requests
from flask import Response


def get_id_token(uid: str):
    cred: Any = credentials.Certificate(
        abspath(
            join(
                dirname(dirname(realpath(__file__))), "config", getenv("FIREBASE_JSON")
            )
        )
    )
    firebase_admin.initialize_app(cred, name="TEST_APP")
    custom_token = auth.create_custom_token(uid).decode("utf-8")
    res: Response = requests.post(
        f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={getenv('FIREBASE_API_KEY')}",
        data=dict(token=custom_token, returnSecureToken=True),
    )
    return res.json().get("idToken")
