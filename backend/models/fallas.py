from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from database import Base

class Falla(Base):
    __tablename__ = "fallas"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)

    logs = relationship("LogFalla", back_populates="falla")
    servicios = relationship("ServicioFalla", back_populates="falla")
