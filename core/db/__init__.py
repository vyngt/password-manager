from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

STORE_PATH = "data/data.db"

engine = create_engine(f"sqlite:///{STORE_PATH}", echo=True, future=True)


def create_tables():

    from .models import Item

    Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
