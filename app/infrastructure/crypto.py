import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2 import PasswordHasher
import bcrypt
from flask import current_app


class CryptoService:
    @staticmethod
    def _get_key() -> bytes:
        # Get key from config or environment, must be 32 bytes for AES-256
        key = current_app.config.get("AES_GCM_KEY")
        if not key:
            key = os.environ.get("AES_GCM_KEY", "01234567890123456789012345678901")
        if isinstance(key, str):
            key = key.encode("utf-8")
        if len(key) != 32:
            key = key[:32].ljust(32, b"0")
        return key

    @classmethod
    def encrypt_data(cls, data: str) -> bytes:
        if not data:
            return b""
        aesgcm = AESGCM(cls._get_key())
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, data.encode("utf-8"), None)
        return nonce + ciphertext

    @classmethod
    def decrypt_data(cls, encrypted_data: bytes) -> str:
        if not encrypted_data:
            return ""
        aesgcm = AESGCM(cls._get_key())
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        try:
            return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
        except Exception:
            return ""

    @staticmethod
    def hash_argon2(password: str) -> str:
        ph = PasswordHasher()
        return ph.hash(password)

    @staticmethod
    def hash_bcrypt(password: str) -> str:
        # bcrypt has a 72-byte limit.
        pwd_bytes = password.encode("utf-8")[:72]
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")
