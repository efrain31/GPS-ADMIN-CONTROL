from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Pieza(Base):
    __tablename__ = "piezas"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    id_opcion = Column(Integer)  # referenciar lectoras, discos, cables o gps_modelos
    nombre = Column(String(150))
    descripcion = Column(Text)
    stock = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint("tipo IN ('LECTORA','DISCO_DURO','CABLE','GPS')", name="chk_tipo_pieza"),
    )

    inventario_interno = relationship("InventarioInterno", back_populates="pieza")
    servicio_piezas = relationship("ServicioPieza", back_populates="pieza")
