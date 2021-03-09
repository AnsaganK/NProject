import sqlalchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from app.models import Base, DATABASE_URL, engine


RolesPermissions = Table(
    'RolesPermissions',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('roleId', Integer, ForeignKey('roles.id')),
    Column('permissionId', Integer, ForeignKey('permissions.id'))
)
