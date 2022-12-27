import secrets
from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

__all__ = ["Encryptor"]


class Encryptor:
    def __init__(self, password: str) -> None:
        self.__password = password

    def __derive(self, password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return b64encode(kdf.derive(password.encode()))

    def encrypt_message(self, message: str, password: str) -> str:
        salt = secrets.token_bytes(16)
        key = self.__derive(password, salt)
        token = b64encode(Fernet(key).encrypt(message.encode()))
        return b64encode(b"%b%b" % (salt, b64decode(token))).decode()

    def decrypt_message(self, enc_message: str, password: str) -> str:
        decoded = b64decode(enc_message.encode())
        salt, cipher_text = decoded[:16], decoded[16:]
        key = self.__derive(password, salt)
        return Fernet(key).decrypt(cipher_text).decode()

    def encrypt(self, data: str):
        return self.encrypt_message(data, self.__password)

    def decrypt(self, enc_data: str):
        return self.decrypt_message(enc_data, self.__password)
