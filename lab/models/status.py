from config import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import ForeignKey


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name


