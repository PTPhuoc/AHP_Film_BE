from sqlalchemy import Column, Integer, String, DateTime
from main.api.database import Base
from sqlalchemy.orm import relationship


class Caculators(Base):
    __tablename__ = "Caculators"

    id = Column(String(255), primary_key=True, unique=True, index=True)
    dateCreate = Column(DateTime, index=True)

    plans = relationship("Plans", back_populates="caculator", cascade="all, delete-orphan")
    criteria = relationship("Criterias", back_populates="caculator", cascade="all, delete-orphan")
    pairofcriterias = relationship("Pair_Of_Criterias", back_populates="caculator", cascade="all, delete-orphan")
    pairofplans = relationship("Pair_Of_Plans", back_populates="caculator", cascade="all, delete-orphan")

