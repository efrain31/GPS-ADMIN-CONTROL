from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base



class ServicioPieza(Base):
    __tablename__ = "servicio_pieza"

    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True)
    pieza_id = Column(Integer, ForeignKey("piezas.id", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(Integer, default=1, nullable=False)

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="chk_cantidad_servicio_pieza"),
    )

    servicio = relationship("Servicio", back_populates="piezas", lazy="joined")
    pieza = relationship("Pieza", back_populates="servicio_piezas", lazy="joined")
