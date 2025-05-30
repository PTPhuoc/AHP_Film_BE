from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from main.api.database import Base
from sqlalchemy.orm import relationship


class Pair_Of_Criterias(Base):
    __tablename__ = "PairOfCriterias"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    caculatorId = Column(String(255), ForeignKey("Caculators.id"), index=True)
    matrix = Column(Text)
    cr = Column(Float, index=True)

    caculator = relationship("Caculators", back_populates="pairofcriterias")

