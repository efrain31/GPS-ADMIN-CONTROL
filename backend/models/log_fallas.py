from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class LogFalla(Base):
    __tablename__ = "log_fallas"

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id"))
    falla_id = Column(Integer, ForeignKey("fallas.id"))
    descripcion = Column(Text)
    fecha_registro = Column(TIMESTAMP)
    activo = Column(Boolean, default=True)

    unidad = relationship("Unidad", back_populates="logs_fallas")
    falla = relationship("Falla", back_populates="logs")
