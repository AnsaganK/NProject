from app.models import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .samples import Samples
from app.models.organization import Organization


SelectionOrganization = Table(
    'SelectionOrganization',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('selectionId', Integer, ForeignKey('selection.id')),
    Column('organizationId', Integer, ForeignKey('organization.id'))
)

SelectionSamples = Table(
    'SelectionSamples',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('selectionId', Integer, ForeignKey('selection.id')),
    Column('samplesId', Integer, ForeignKey('samples.id'))
)


class Selection(Base):
    __tablename__ = "selection"

    id = Column(Integer, primary_key=True)
    organization = relationship("Organization", secondary=SelectionOrganization, backref="selection")
    samples = relationship("Samples", secondary=SelectionSamples, backref="selection")
    amount = Column(Integer)
    date = Column(BigInteger)
    status = Column(String)

    def __repr__(self):
        return "<selection ({})>".format(self.id)
