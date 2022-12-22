from .db import create_tables

__all__ = [
    "boot",
]


def boot():
    create_tables()
