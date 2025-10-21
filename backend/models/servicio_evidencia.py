from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoEvidenciaEnum(enum.Enum):
    ANTES = "ANTES"
    DESPUES = "DESPUES"
    PROCESO = "PROCESO"

class ServicioEvidencia(Base):
    __tablename__ = "servicio_evidencia"

    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True)
    evidencia_id = Column(Integer, ForeignKey("evidencias.id", ondelete="CASCADE"), primary_key=True)
    tipo = Column(Enum(TipoEvidenciaEnum), nullable=False)

    servicio = relationship("Servicio", back_populates="evidencias")
    evidencia = relationship("Evidencia", back_populates="servicios")
