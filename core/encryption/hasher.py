from argon2 import PasswordHasher
from argon2 import exceptions as ex

__all__ = ["hash_password", "verify_password"]

PH = PasswordHasher()


def hash_password(password: str) -> str | None:
    try:
        return PH.hash(password)
    except ex.HashingError:
        return None


def verify_password(hash: str, password: str) -> bool:
    try:
        return PH.verify(hash=hash, password=password)
    except ex.VerifyMismatchError:
        return False
    except ex.InvalidHash:
        return False
    except ex.VerificationError:
        return False
