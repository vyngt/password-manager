from sqlalchemy import Column, Integer, Text

from . import Base


__all__ = ["Item"]


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    url = Column(Text)
    username = Column(Text)
    password = Column(Text)

    def __repr__(self):
        return f"Item(id={self.id!r}, name={self.name!r}, username={self.username!r})"
