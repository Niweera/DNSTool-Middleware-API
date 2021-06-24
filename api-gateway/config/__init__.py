import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_ENV: str = os.environ.get("FLASK_ENV")
    PROPAGATE_EXCEPTIONS: bool = True
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = True
    FIREBASE_JSON: str = os.environ.get("FIREBASE_JSON")
    FIREBASE_DATABASE_URL: str = os.environ.get("FIREBASE_DATABASE_URL")
    GCS_JSON: str = os.environ.get("GCS_JSON")
    GCS_BUCKET_NAME: str = os.environ.get("GCS_BUCKET_NAME")
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_PORT: str = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS: str = False
    MAIL_USE_SSL: str = True
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.environ.get("MAIL_DEFAULT_SENDER")
