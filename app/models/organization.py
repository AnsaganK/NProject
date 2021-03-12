from config import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .organizationUser import OrganizationUser

class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    bin = Column(String)

    def __repr__(self):
        return "<organization ({})>".format(self.name)