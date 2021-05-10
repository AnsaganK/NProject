from config import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime

from lab.models.order import OrderElementsType, OrderGroupElementsType


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    gost = Column(String)


    def __repr__(self):
        return self.name


class ElementType(Base):
    __tablename__ = "ElementType"

    id = Column(Integer, primary_key=True)
    typeId = Column(Integer, ForeignKey('types.id'))
    type = relationship("Type", cascade="all,delete", backref="elements")
    elementId = Column(Integer, ForeignKey('elements.id'))
    element = relationship("Elements",  backref="types")

    orderGroups = relationship("OrderGroup", secondary=OrderGroupElementsType, back_populates="elementTypes")
    orders = relationship("Order", secondary=OrderElementsType, back_populates="elementTypes")

    def __repr__(self):
        return "<ElementType ({})>".format(self.id)


class ElementErrorRange(Base):
    __tablename__ = "ElementErrorRange"

    id = Column(Integer, primary_key=True)
    errorRangeId = Column(Integer, ForeignKey("errorRanges.id"))
    errorRange = relationship("ErrorRange", backref="error_ranges")

    elementTypeId = Column(Integer, ForeignKey("ElementType.id"))
    elementType = relationship("ElementType", backref="element_types")

    def __repr__(self):
        return "<ElementErrorRange ({})>".format(self.id)


class ErrorRange(Base):
    __tablename__ = "errorRanges"

    id = Column(Integer, primary_key=True)
    value = Column(String)
    of = Column(Float)
    to = Column(Float)

    def __repr__(self):
        return self.name

class Range(Base):
    __tablename__ = "range"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    of = Column(Float)
    to = Column(Float)

    def __repr__(self):
        return self.name


class ElementColor(Base):
    __tablename__ = "ElementColor"

    id = Column(Integer, primary_key=True)
    elementTypeId = Column(Integer, ForeignKey("ElementType.id"))
    elementType = relationship("ElementType", cascade="all,delete",  backref="color")
    rangeColorId = Column(Integer, ForeignKey("RangeColor.id"))
    rangeColor = relationship("RangeColor", cascade="all,delete",  backref="element")

    def __repr__(self):
        return "<ElementColor ({})>".format(self.id)

class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)

    def __repr__(self):
        return self.name


class RangeColor(Base):
    __tablename__ = "RangeColor"

    id = Column(Integer, primary_key=True)

    rangeId = Column(Integer, ForeignKey('range.id'))
    range = relationship("Range", cascade="all,delete",  backref="color")
    colorId = Column(Integer, ForeignKey('colors.id'))
    color = relationship("Color",  backref="range")

    def __repr__(self):
        return "<RangeColor ({})>".format(self.id)

class Elements(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String)
    date = Column(BigInteger)
    standard = Column(Boolean, default=False)

    def __repr__(self):
        return "<element ({})>".format(self.name)