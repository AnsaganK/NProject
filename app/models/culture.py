from config import Base
from sqlalchemy import Column, Integer, String, Boolean


class Culture(Base):
    __tablename__ = "cultures"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    default = Column(Boolean)
    shortName = Column(String)
    description = Column(String)
    fillColor = Column(String)

    def __repr__(self):
        return "<Culture ({})>".format(self.name)