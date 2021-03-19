from config import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import ForeignKey


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    role_edit_id = Column(Integer, ForeignKey("roles.id"))


    color = Column(String)

    def __repr__(self):
        return self.name
