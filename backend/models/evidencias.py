from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Evidencia(Base):
    __tablename__ = "evidencias"

    id = Column(Integer, primary_key=True, index=True)
    url_imagen = Column(Text)
    descripcion = Column(Text)
    fecha = Column(TIMESTAMP)

    servicios = relationship("ServicioEvidencia", back_populates="evidencia")
