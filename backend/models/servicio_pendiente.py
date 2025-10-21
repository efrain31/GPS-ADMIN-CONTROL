from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from database import Base
import enum

class EstadoPendienteEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    FINALIZADO = "FINALIZADO"

class ServicioPendiente(Base):
    __tablename__ = "servicio_pendiente"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), nullable=False)
    usuario_id_admin = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Enum(EstadoPendienteEnum), default=EstadoPendienteEnum.PENDIENTE, nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    servicio = relationship("Servicio", back_populates="pendientes")
    usuario_admin = relationship("Usuario", foreign_keys=[usuario_id_admin], back_populates="pendientes_asignados")
    tecnico = relationship("Usuario", foreign_keys=[tecnico_id], back_populates="pendientes_tecnico")
