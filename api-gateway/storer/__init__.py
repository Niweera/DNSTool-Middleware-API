import io
from os.path import abspath, join, dirname, realpath
from typing import Any, List, Dict, Iterator
from google.api_core.page_iterator import HTTPIterator
from google.cloud import storage
from google.cloud.storage import Bucket, Blob
from config import Config
from middleware.error_handling import write_log, InternalServerError, NotFoundError
from google.resumable_media.requests import ChunkedDownload
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import urllib.parse
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE_PATH: str = abspath(
    join(dirname(dirname(realpath(__file__))), "config", Config.GCS_JSON)
)
storage_client: Any = storage.Client.from_service_account_json(
    SERVICE_ACCOUNT_FILE_PATH
)
bucket: Bucket = storage_client.get_bucket(Config.GCS_BUCKET_NAME)
CHUNK_SIZE: int = 1024 * 1024 * 10  # 10MB


class Storer:
    """
    Class to retrieve data from persistent storage such as Google Cloud Bucket
    """

    def __init__(self) -> None:
        self.bucket: Bucket = bucket

    def get_file_paths_for_scan(self, scan: Dict[str, str]) -> List[str]:
        try:
            prefix: str = f"{scan.get('region')}/{scan.get('zone')}/"
            blobs: HTTPIterator = storage_client.list_blobs(self.bucket, prefix=prefix)
            file_paths: List[str] = [blob.name for blob in blobs if blob.name != prefix]
            return file_paths
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def download_file(self, path: str) -> Iterator:
        try:
            file_blob: Blob = self.bucket.blob(path)

            if not file_blob.exists():
                raise NotFoundError

            blob_name: str = urllib.parse.quote(file_blob.name, safe="")
            media_url: str = f"https://www.googleapis.com/download/storage/v1/b/{self.bucket.name}/o/{blob_name}?alt=media"

            credentials: Credentials = (
                service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE_PATH
                )
            )

            scoped_credentials: Credentials = credentials.with_scopes(
                ["https://www.googleapis.com/auth/devstorage.read_only"]
            )
            transport: AuthorizedSession = AuthorizedSession(scoped_credentials)

            stream: io.BytesIO = io.BytesIO()
            download: ChunkedDownload = ChunkedDownload(media_url, CHUNK_SIZE, stream)

            start_position: int = 0
            while not download.finished:
                download.consume_next_chunk(transport)
                stream.seek(start_position)
                end_position: int = start_position + CHUNK_SIZE
                start_position = end_position
                yield stream.read(end_position)

        except NotFoundError:
            raise NotFoundError
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    def get_download_file_mime_type(self, path: str) -> str:
        try:
            file_blob: Blob = self.bucket.get_blob(path)
            if not file_blob.exists():
                raise NotFoundError
            return file_blob.content_type
        except NotFoundError:
            raise NotFoundError
        except Exception as e:
            write_log("error", e)
            raise InternalServerError
