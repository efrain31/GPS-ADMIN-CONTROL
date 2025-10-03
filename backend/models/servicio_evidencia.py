from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioEvidencia(Base):
    __tablename__ = "servicio_evidencia"

    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True)
    evidencia_id = Column(Integer, ForeignKey("evidencias.id", ondelete="CASCADE"), primary_key=True)
    tipo = Column(String(50))

    servicio = relationship("Servicio", back_populates="evidencias")
    evidencia = relationship("Evidencia", back_populates="servicios")
