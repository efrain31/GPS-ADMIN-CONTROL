from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioPendiente(Base):
    __tablename__ = "servicio_pendiente"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"))
    usuario_id_admin = Column(Integer, ForeignKey("usuarios.id"))
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"))
    estado = Column(String(50))
    fecha_registro = Column(TIMESTAMP)

    servicio = relationship("Servicio", back_populates="pendientes")
    usuario_admin = relationship("Usuario", foreign_keys=[usuario_id_admin], back_populates="pendientes_asignados")
    tecnico = relationship("Usuario", foreign_keys=[tecnico_id], back_populates="pendientes_tecnico")
