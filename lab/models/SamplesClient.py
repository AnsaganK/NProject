from sqlalchemy import ForeignKey, Table
from app.models import Base, DATABASE_URL, engine
from sqlalchemy import Integer, String, Column


SamplesClient = Table(
    'SamplesClient',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('samplesId', Integer, ForeignKey('samples.id')),
    Column('clientId', Integer, ForeignKey('organization.id'))
)
