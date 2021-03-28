from config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class WorkSubType(Base):
    __tablename__ = "workSubType"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    default = Column(Boolean)
    groupId = Column(Integer, ForeignKey('workType.id'))
    group = relationship("WorkType", backref="subTypes")

