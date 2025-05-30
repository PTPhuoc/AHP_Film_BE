from sqlalchemy import Column, Integer, String, Unicode, Float, ForeignKey, Text
from main.api.database import Base
from sqlalchemy.orm import relationship


class Pair_Of_Plans(Base):
    __tablename__ = "PairOfPlans"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    caculatorId = Column(String(255), ForeignKey("Caculators.id"), index=True)
    matrix = Column(Text)
    name = Column(Unicode(255), index=True)
    cr = Column(Float, index=True)

    caculator = relationship("Caculators", back_populates="pairofplans")

