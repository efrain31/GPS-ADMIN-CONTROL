from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class ServicioHistorial(Base):
    __tablename__ = "servicio_historial"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    accion = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    servicio = relationship("Servicio", back_populates="historial")
    usuario = relationship("Usuario", back_populates="servicio_historial")
