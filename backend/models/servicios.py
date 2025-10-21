# models/servicios.py
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class EstadoServicioEnum(enum.Enum):
    ACRIVO = "ACTIVO"
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"

class PrioridadEnum(enum.Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id_levanta = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario_id_aprueba = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # técnico asignado o quien aprueba
    unidad_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    planta_id = Column(Integer, ForeignKey("plantas.id"), nullable=True)  # <-- nueva columna
  
    cambios = Column(Text, nullable=True)
    items = Column(Text, nullable=True)
    comentarios = Column(Text, nullable=True)
    fecha_alta = Column(Date, nullable=False)
    fecha_liberacion = Column(Date, nullable=True)
    estado = Column(Enum(EstadoServicioEnum), default=EstadoServicioEnum.PENDIENTE, nullable=True )
    prioridad = Column(Enum(PrioridadEnum), default=PrioridadEnum.MEDIA)
    domiciliado = Column(Boolean, default=False)
    latitud = Column(DECIMAL(10, 6), nullable=True)
    longitud = Column(DECIMAL(10, 6), nullable=True)
    pendiente = Column(Boolean, default=False)
    reasignado_admin = Column(Boolean, default=False)
    bloqueado = Column(Boolean, default=False)  # si admin la bloquea (pausa que solo admin deshace)

    unidad = relationship("Unidad", back_populates="servicios")
    usuario_levanta = relationship("Usuario", foreign_keys=[usuario_id_levanta], back_populates="servicios_levantados")
    usuario_aprueba = relationship("Usuario", foreign_keys=[usuario_id_aprueba], back_populates="servicios_aprobados")
    planta = relationship("Planta")
    
    pendientes = relationship("ServicioPendiente", back_populates="servicio")
    fallas = relationship("ServicioFalla", back_populates="servicio")
    piezas = relationship("ServicioPieza", back_populates="servicio")
    historial = relationship("ServicioHistorial", back_populates="servicio")
    evidencias = relationship("ServicioEvidencia", back_populates="servicio")
    tiempos = relationship("ServicioTiempo", back_populates="servicio")
    extensiones = relationship("ServicioExtension", back_populates="servicio")
