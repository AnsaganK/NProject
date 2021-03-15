from config import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.organization import Organization


FieldOrganization = Table(
    'FieldOrganization',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('FieldId', Integer, ForeignKey('fields.id')),
    Column('organizationId', Integer, ForeignKey('organization.id'))
)


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', backref="fields") #lazy='subquery')
    kadNumber = Column(String, unique=True)
    urlShpFile = Column(String)
    districtId = Column(String)
    GeoJson = Column(JSON)

    def __repr__(self):
        return "<Field ({})>".format(self.id)


