from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioExtension(Base):
    __tablename__ = "servicio_extension"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    duracion = Column(Text)
    fecha_solicitud = Column(TIMESTAMP)
    aprobado = Column(Boolean, default=False)

    servicio = relationship("Servicio", back_populates="extensiones")
    usuario = relationship("Usuario", back_populates="extensiones_servicios")
