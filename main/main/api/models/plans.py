from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from main.api.database import Base
from sqlalchemy.orm import relationship


class Plans(Base):
    __tablename__ = "Plans"

    id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    caculatorId = Column(String(255), ForeignKey("Caculators.id"), index=True)
    name = Column(String(255), index=True)
    index = Column(Integer, index=True)

    caculator = relationship("Caculators", back_populates="plans")


