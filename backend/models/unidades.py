from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Unidad(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"))
    tipo = Column(String(100), nullable=False)
    caracteristicas = Column(Text)
    ignicion_movimiento = Column(String(50))

    
    #__table_args__ = (
     #   CheckConstraint(
      #      "ignicion_movimiento IS NULL OR ignicion_movimiento IN ('IGNICION', 'MOVIMIENTO')",
       #     name="chk_ignicion_movimiento"
        #    ),
        #)


    empresa = relationship("Empresa", back_populates="unidades")
    inventario = relationship("InventarioInterno", back_populates="unidad")
    logs_fallas = relationship("LogFalla", back_populates="unidad")
    servicios = relationship("Servicio", back_populates="unidad")
    registros = relationship("Usuario", back_populates="unidad")
    piezas_registro = relationship("UnidadPiezaRegistro", back_populates="unidad")

