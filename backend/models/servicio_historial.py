from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioHistorial(Base):
    __tablename__ = "servicio_historial"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    accion = Column(Text)
    fecha = Column(TIMESTAMP)

    servicio = relationship("Servicio", back_populates="historial")
    usuario = relationship("Usuario", back_populates="servicio_historial")
