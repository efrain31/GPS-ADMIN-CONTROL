from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from database import Base

class UnidadPiezaRegistro(Base):
    __tablename__ = "unidad_pieza_registro"

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id", ondelete="CASCADE"), nullable=False)
    inventario_id = Column(Integer, ForeignKey("inventario_interno.id", ondelete="CASCADE"), nullable=False)
    cantbus = Column(String(50), nullable=False)
    danado = Column(Boolean, default=False, nullable=False)
    fecha_actualizacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    motivo_cambio = Column(Text, nullable=True)

    inventario = relationship("InventarioInterno", back_populates="registros")
    usuario = relationship("Usuario", back_populates="piezas_registro")
    unidad = relationship("Unidad", back_populates="piezas_registro")

