# models/unidades.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Unidad(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"))
    planta_id = Column(Integer, ForeignKey("plantas.id", ondelete="CASCADE")) 
    tipo = Column(String(100), nullable=False)
    planta = Column(String(100), nullable=False)
    caracteristicas = Column(Text)
    ignicion_movimiento = Column(String(50))

   
    empresa = relationship("Empresa", back_populates="unidades")
    planta = relationship("Planta", back_populates="unidades") 
 
    inventario = relationship("InventarioInterno", back_populates="unidad")
    logs_fallas = relationship("LogFalla", back_populates="unidad")
    servicios = relationship("Servicio", back_populates="unidad")
    registros = relationship("Usuario", back_populates="unidad")
    piezas_registro = relationship("UnidadPiezaRegistro", back_populates="unidad")



    inventario_interno = relationship("InventarioInterno",back_populates="unidad",overlaps="inventario" )
