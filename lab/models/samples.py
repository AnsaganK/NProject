from app.models import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import relationship
import datetime
from .SamplesClient import SamplesClient
from .SamplesElement import SamplesElement
from app.models.organization import Organization
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

# Пробы
class Samples(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True)
    client = relationship("Organization", secondary=SamplesClient, backref="samples")
    amount = Column(Integer)
    standard = Column(Boolean)
    elements = relationship("Elements", secondary=SamplesElement, backref="samples")
    date = Column(BigInteger)

    def __repr__(self):
        return "<sample ({})>".format(self.id)