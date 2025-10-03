from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ServicioPieza(Base):
    __tablename__ = "servicio_pieza"

    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True)
    pieza_id = Column(Integer, ForeignKey("piezas.id"), primary_key=True)
    cantidad = Column(Integer, default=1)

    servicio = relationship("Servicio", back_populates="piezas")
    pieza = relationship("Pieza", back_populates="servicio_piezas")
