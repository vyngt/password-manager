from gui import open_window
from .db import create_tables

__all__ = [
    "boot",
]


def boot():
    create_tables()
    open_window()
