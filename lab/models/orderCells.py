from config import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table, JSON
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import ForeignKey

OrderCells = Table(
    'OrderCells',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('CellCode', Integer),
    Column('status', String)
)