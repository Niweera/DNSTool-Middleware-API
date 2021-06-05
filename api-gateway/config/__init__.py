import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_ENV = os.environ.get("FLASK_ENV")
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    FIREBASE_JSON = os.environ.get("FIREBASE_JSON")
    FIREBASE_DATABASE_URL = os.environ.get("FIREBASE_DATABASE_URL")
    GCS_JSON = os.environ.get("GCS_JSON")
    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
