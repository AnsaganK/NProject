from config import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship
import datetime
#from lab.models.order import OrderCells

class CellsHistory(Base):
    __tablename__ = "CellsHistory"

    id = Column(Integer, primary_key=True)
    orderId = Column(Integer, ForeignKey("OrderCells.id"))
    order = relationship("OrderCells", backref="history")
    status = Column(String)
    date = Column(BigInteger)

    def __repr__(self):
        return "<history ({})>".format(self.id)


class Cells(Base):
    __tablename__ = "cells"

    id = Column(Integer, primary_key=True)
    code = Column(Integer)

    def __repr__(self):
        return "<cell ({})>".format(self.id)
