from config import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship
import datetime

CellsStatus = Table(
    'CellsStatus',
    Base.metadata,
    Column('cellId', Integer, ForeignKey('cells.id')),
    Column('statusId', Integer, ForeignKey('status.id'))
)

class Cells(Base):
    __tablename__ = "cells"

    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    status = relationship('Status', secondary=CellsStatus, backref="cells")

    def __repr__(self):
        return "<cell ({})>".format(self.id)
