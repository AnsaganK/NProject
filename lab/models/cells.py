from config import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship
import datetime


class Cells(Base):
    __tablename__ = "cells"

    id = Column(Integer, primary_key=True)
    code = Column(Integer)

    def __repr__(self):
        return "<cell ({})>".format(self.id)
