from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class InventarioInterno(Base):
    __tablename__ = "inventario_interno"

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id", ondelete="CASCADE"), nullable=False)
    pieza_id = Column(Integer, ForeignKey("piezas.id", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    danado = Column(Boolean, default=False, nullable=False)
    fecha_actualizacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    unidad = relationship("Unidad", back_populates="inventario")
    pieza = relationship("Pieza", back_populates="inventario_interno")
    registros = relationship("UnidadPiezaRegistro", back_populates="inventario")
