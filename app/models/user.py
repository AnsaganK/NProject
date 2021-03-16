import sqlalchemy
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from config import Base, DATABASE_URL, engine
from app.models.UserRole import UsersRoles
from .organizationUser import OrganizationUser

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String)
    organizationId = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', backref="user")
    roles = relationship("Role", secondary=UsersRoles, backref="users")

    def __repr__(self):
        return "<User ({0})>".format(self.username)




