import sqlalchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy import Integer, String, Column
from app.models import Base, DATABASE_URL, engine


OrganizationUser = Table(
    'OrganizationParent',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('OrganizationParentId', Integer, ForeignKey('organization.id')),
    Column('OrganizationChildrenId', Integer, ForeignKey('organization.id'))
)
