import sqlalchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy import Integer, String, Column
from app.models import Base, DATABASE_URL, engine


OrganizationUser = Table(
    'OrganizationUser',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('OrganizationId', Integer, ForeignKey('organization.id')),
    Column('UserId', Integer, ForeignKey('users.id'))
)
