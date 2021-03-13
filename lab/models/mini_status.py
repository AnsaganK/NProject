from config import Base
from sqlalchemy import String, Column, Integer


class MiniStatus(Base):
    __tablename__ = "MiniStatus"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name
