from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from main.api.database import Base
from sqlalchemy.orm import relationship


class Criterias(Base):
    __tablename__ = "Criterias"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    caculatorId = Column(String(255), ForeignKey("Caculators.id"), index=True)
    name = Column(String(255), unique=True, index=True)
    index = Column(Integer, index=True)

    caculator = relationship("Caculators", back_populates="criteria")
