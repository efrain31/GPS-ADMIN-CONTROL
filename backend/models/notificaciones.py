from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id")) 
    mensaje = Column(String(250), nullable=False)
    tipo = Column(String(50))  # Por ejemplo: "servicio", "unidad", "pieza"
    referencia_id = Column(Integer)  # ID de la entidad relacionada (opcional)
    leida = Column(Boolean, default=False)
    fecha = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="notificaciones")
