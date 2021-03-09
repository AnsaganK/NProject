import sqlalchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from app.models import Base, DATABASE_URL, engine


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)

    def __repr__(self):
        return "<Permission ({})>".format(self.name)

