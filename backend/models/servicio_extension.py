from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class ServicioExtension(Base):
    __tablename__ = "servicio_extension"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    duracion = Column(Text, nullable=False)
    fecha_solicitud = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    aprobado = Column(Boolean, default=False, nullable=False)

    servicio = relationship("Servicio", back_populates="extensiones")
    usuario = relationship("Usuario", back_populates="extensiones_servicios")
