from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioFalla(Base):
    __tablename__ = "servicio_falla"

    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True)
    falla_id = Column(Integer, ForeignKey("fallas.id", ondelete="CASCADE"), primary_key=True)

    servicio = relationship("Servicio", back_populates="fallas")
    falla = relationship("Falla", back_populates="servicios")
