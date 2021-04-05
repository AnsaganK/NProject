from config import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .organizationUser import OrganizationUser

class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    bin = Column(String)

    selectedSeasonId = Column(Integer, ForeignKey("seasons.id"))
    selectedSeason = relationship("Season", backref="organizations")

    def __repr__(self):
        return "<organization ({})>".format(self.name)


#Organization.field = relationship('Field', back_populates="organization")
#Organization.user = relationship('User', back_populates="organization")