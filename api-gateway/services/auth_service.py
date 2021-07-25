import hashlib
from typing import Tuple
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from middleware.error_handling import write_log, InternalServerError


class AuthService:
    @staticmethod
    def generate_rsa_key_pair() -> Tuple[bytes, bytes]:
        try:
            key: RsaKey = RSA.generate(2048)
            private_key: bytes = key.export_key(
                pkcs=8, protection="scryptAndAES128-CBC"
            )
            public_key: bytes = key.publickey().export_key()
            return private_key, public_key
        except Exception as e:
            write_log("error", e)
            raise InternalServerError

    @staticmethod
    def generate_private_key_id() -> str:
        try:
            key: bytes = get_random_bytes(16)
            hex_digest: str = hashlib.sha256(key).hexdigest()
            return hex_digest
        except Exception as e:
            write_log("error", e)
            raise InternalServerError
