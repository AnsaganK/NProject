from sqlalchemy import Column, Integer, String
from config import Base


class IrrigationType(Base):
    __tablename__ = "irrigationTypes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<irrirgationType ({})>".format(self.name)