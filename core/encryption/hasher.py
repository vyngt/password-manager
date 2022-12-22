from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError

__all__ = ["hash_password", "verify_password"]

PH = PasswordHasher()


def hash_password(password: str) -> str | None:
    try:
        return PH.hash(password)
    except HashingError:
        return None


def verify_password(hash: str, password: str) -> bool:
    try:
        return PH.verify(hash=hash, password=password)
    except VerifyMismatchError:
        return False
