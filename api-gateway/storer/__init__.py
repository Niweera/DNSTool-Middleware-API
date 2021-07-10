from os.path import abspath, join, dirname, realpath
from typing import Any
from google.cloud import storage
from google.cloud.storage import Bucket
from config import Config


storage_client: Any = storage.Client.from_service_account_json(
    abspath(join(dirname(dirname(realpath(__file__))), "config", Config.GCS_JSON))
)
bucket: Bucket = storage_client.get_bucket(Config.GCS_BUCKET_NAME)


class Storer:
    """
    Class to retrieve data from persistent storage such as Google Cloud Bucket
    """

    def __init__(self) -> None:
        self.bucket: Bucket = bucket
