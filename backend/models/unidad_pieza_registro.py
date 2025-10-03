from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class UnidadPiezaRegistro(Base):
    __tablename__ = "unidad_pieza_registro"

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id", ondelete="CASCADE"))
    inventario_id = Column(Integer, ForeignKey("inventario_interno.id", ondelete="CASCADE"))
    cantbus = Column(String(50))
    danado = Column(Boolean, default=False)
    fecha_actualizacion = Column(TIMESTAMP)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    motivo_cambio = Column(Text)

  
    inventario = relationship("InventarioInterno", back_populates="registros")
    usuario = relationship("Usuario", back_populates="piezas_registro")
    unidad = relationship("Unidad", back_populates="piezas_registro")
