from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class LogFalla(Base):
    __tablename__ = "log_fallas"

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id", ondelete="CASCADE"), nullable=False)
    falla_id = Column(Integer, ForeignKey("fallas.id", ondelete="CASCADE"), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    unidad = relationship("Unidad", back_populates="logs_fallas")
    falla = relationship("Falla", back_populates="logs")
