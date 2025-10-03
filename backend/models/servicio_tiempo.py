from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioTiempo(Base):
    __tablename__ = "servicio_tiempo"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    accion = Column(Text)
    timestamp = Column(TIMESTAMP)

    servicio = relationship("Servicio", back_populates="tiempos")
    usuario = relationship("Usuario", back_populates="tiempos_servicios")
