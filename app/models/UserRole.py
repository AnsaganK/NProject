import sqlalchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy import Integer, String, Column
from app.models import Base


UsersRoles = Table(
    'UsersRoles',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('userId', Integer, ForeignKey('users.id')),
    Column('roleId', Integer, ForeignKey('roles.id'))
)
