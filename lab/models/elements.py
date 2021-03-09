from app.models import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.orm import relationship
import datetime


class Elements(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String)
    date = Column(BigInteger)
    isMain = Column(Boolean, default=False)

    def __repr__(self):
        return "<element ({})>".format(self.name)