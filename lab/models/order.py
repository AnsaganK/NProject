from config import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table, JSON
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

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    organization = relationship('Organization', secondary=OrderOrganization, backref="orders")
    elements = relationship('Elements', secondary=OrderElements, backref="orders")
    date = Column(Integer)
    grid = Column(JSON)
    cellCount = Column(Integer)


    def __repr__(self):
        return "<order ({})>".format(self.id)
