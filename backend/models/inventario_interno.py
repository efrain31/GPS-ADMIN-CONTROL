from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class InventarioInterno(Base):
    __tablename__ = "inventario_interno"

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id", ondelete="CASCADE"))
    pieza_id = Column(Integer, ForeignKey("piezas.id", ondelete="CASCADE"))
    cantidad = Column(Integer, default=1)
    danado = Column(Boolean, default=False)
    fecha_actualizacion = Column(TIMESTAMP)

    unidad = relationship("Unidad", back_populates="inventario")
    pieza = relationship("Pieza", back_populates="inventario_interno")
    registros = relationship("UnidadPiezaRegistro", back_populates="inventario")
