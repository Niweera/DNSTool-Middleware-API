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
