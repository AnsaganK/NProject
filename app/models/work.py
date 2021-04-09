from config import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, BigInteger, Table
from sqlalchemy.orm import relationship

WorkUsers = Table(
    'WorkUsers',
    Base.metadata,
    Column('workId', Integer, ForeignKey('work.id')),
    Column('userId', Integer, ForeignKey('users.id'))
)

WorkCars = Table(
    'WorkCars',
    Base.metadata,
    Column('workId', Integer, ForeignKey('work.id')),
    Column('carId', Integer, ForeignKey('cars.id'))
)

class Work(Base):
    __tablename__ = "work"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    fieldId = Column(Integer, ForeignKey('fields.id'))
    field = relationship("Field", backref="works", foreign_keys=[fieldId])
    startDate = Column(BigInteger)
    endDate = Column(BigInteger)

    statusId = Column(Integer, ForeignKey('MiniStatus.id'))
    status = relationship("MiniStatus", backref="works", foreign_keys=[statusId])

    workTypeId = Column(Integer, ForeignKey("workType.id"))
    workType = relationship("WorkType", backref="works", foreign_keys=[workTypeId])

    workSubTypeId = Column(Integer, ForeignKey("workSubType.id"))
    workSubType = relationship("WorkSubType", backref="works", foreign_keys=[workSubTypeId])

    users = relationship("User", secondary=WorkUsers, backref="works")
    cars = relationship("Car", secondary=WorkCars, backref="works")

    geoJson = Column(JSON)