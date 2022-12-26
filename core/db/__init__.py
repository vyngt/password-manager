from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from conf import settings

Base = declarative_base()

engine = create_engine(
    f"sqlite:///{settings.DATA_LOCATION}", echo=settings.DEBUG, future=True
)


def create_tables():

    from .models import Item

    Base.metadata.create_all(engine)


def get_session():
    return Session(engine)
