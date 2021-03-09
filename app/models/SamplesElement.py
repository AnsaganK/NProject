from sqlalchemy import ForeignKey, Table
from app.models import Base, DATABASE_URL, engine
from sqlalchemy import Integer, String, Column


SamplesElement = Table(
    'SamplesElement',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('samplesId', Integer, ForeignKey('samples.id')),
    Column('elementId', Integer, ForeignKey('elements.id'))
)
