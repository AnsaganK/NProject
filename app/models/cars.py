from config import Base
from sqlalchemy import Column, Integer, ForeignKey, String

from sqlalchemy.orm import relationship, subqueryload


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)
    organizationId = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', backref='cars')
    terminalId = Column(String)

    def __repr__(self):
        return "<Car ({})>".format(self.name)