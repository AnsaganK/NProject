from config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class FieldCultureSeason(Base):
    __tablename__ = "FieldCultureSeason"

    id = Column(Integer, primary_key=True)

    fieldId = Column(Integer, ForeignKey('fields.id'))
    field = relationship("Field", backref="cultureSeason")

    cultureId = Column(Integer, ForeignKey('cultures.id'))
    culture = relationship('Culture', backref="fieldSeason")

    sort = Column(String)

    seasonId = Column(Integer, ForeignKey('seasons.id'))
    season = relationship('Season', backref="cultureField")

    irrigationTypeId = Column(Integer, ForeignKey('irrigationTypes.id'))
    irrigationType = relationship('IrrigationType', backref="field")

    tillageId = Column(Integer, ForeignKey('tillages.id'))
    tillage = relationship("Tillage", backref="field")

    sowingDate = Column(BigInteger)
    cleaningDate = Column(BigInteger)

    prolificness = Column(Integer)
    harvest = Column(Integer)
