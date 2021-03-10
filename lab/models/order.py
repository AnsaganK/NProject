from app.models import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import ForeignKey
from .samples import Samples

OrderSamples = Table(
    'OrderSamples',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('samplesId', Integer, ForeignKey('samples.id'))
)

OrderElements = Table(
    'OrderElements',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('elementsId', Integer, ForeignKey('elements.id'))
)

OrderOrganization = Table(
    'OrderOrganization',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('organizationId', Integer, ForeignKey('organization.id'))
)

OrderField = Table(
    'OrderField',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('orderId', Integer, ForeignKey('orders.id')),
    Column('fieldId', Integer, ForeignKey('fields.id'))
)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    samples = relationship('Sample', secondary=OrderSamples, backref="orders")
    elementsId = relationship('Element', secondary=OrderElements, backref="orders")
    organization = relationship('Organization', secondary=OrderOrganization, backref="orders")
    field = relationship('Field', secondary=OrderField, backref="orders")
    grid = Column(String)

    def __repr__(self):
        return "<order ({})>".format(self.id)
