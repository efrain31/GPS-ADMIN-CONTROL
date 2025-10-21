from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Planta(Base):
    __tablename__ = "plantas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(Text)

    unidades = relationship("Unidad", back_populates="planta")
    servicios = relationship("Servicio", back_populates="planta")