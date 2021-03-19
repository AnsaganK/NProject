from config import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table, JSON, Float
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import ForeignKey

OrderElements = Table(
    'OrderElements',
    Base.metadata,
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('elementId', Integer, ForeignKey('elements.id'))
)

OrderOrganization = Table(
    'OrderOrganization',
    Base.metadata,
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('organizationId', Integer, ForeignKey('organization.id'))
)

#OrderCells = Table(
#    'OrderCells',
#    Base.metadata,
#    Column('id', Integer, primary_key=True),
#    Column('orderId', Integer, ForeignKey('orders.id')),
#    Column('cellId', Integer, ForeignKey('cells.id')),
#)


OrderField = Table(
    'OrderField',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('fieldId', Integer, ForeignKey('fields.id')),
)

class OrderCells(Base):
    __tablename__ = "OrderCells"
    id = Column(Integer, primary_key=True)
    order = relationship('Order', backref="cells")
    orderId = Column(Integer, ForeignKey('orders.id'))
    cell = relationship('Cells', backref="order")
    cellId = Column(Integer, ForeignKey('cells.id'))
    status = Column(String)

    date = Column(BigInteger)

    def __repr__(self):
        return "<orderCells ({})>".format(self.id)


class OrderCellsResult(Base):
    __tablename__ = "OrderCellsResult"

    id = Column(Integer, primary_key=True)
    orderCell = relationship("OrderCells", backref="result")
    orderCellId = Column(Integer, ForeignKey("OrderCells.id"))
    element = relationship("Elements", backref="result")
    elementId = Column(Integer, ForeignKey("elements.id"))

    result = Column(Float)
    date = Column(BigInteger)

    def __repr__(self):
        return "result ({})".format(self.id)

class OrderGroup(Base):
    __tablename__ = "OrderGroup"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    organizationId = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', backref="orderGroup")
    date = Column(BigInteger)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    organizationId = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', backref="orders")
    elements = relationship('Elements', secondary=OrderElements, backref="orders")
    fieldId = Column(Integer, ForeignKey('fields.id'))
    field = relationship('Field', backref="orders")
    date = Column(BigInteger)
    grid = Column(JSON)
    way = Column(JSON)
    cellCount = Column(Integer)
    
    groupId = Column(Integer, ForeignKey("OrderGroup.id"))
    group = relationship('OrderGroup', backref="orders")


    def __repr__(self):
        return "<order ({})>".format(self.id)
