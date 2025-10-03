from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id_levanta = Column(Integer, ForeignKey("usuarios.id"))
    usuario_id_aprueba = Column(Integer, ForeignKey("usuarios.id"))
    unidad_id = Column(Integer, ForeignKey("unidades.id"))
    cambios = Column(Text)
    items = Column(Text)
    comentarios = Column(Text)
    fecha_alta = Column(Date)
    fecha_liberacion = Column(Date)
    estado = Column(String(50))
    domiciliado = Column(Boolean, default=False)
    latitud = Column(DECIMAL(10, 6))
    longitud = Column(DECIMAL(10, 6))
    pendiente = Column(Boolean, default=False)
    reasignado_admin = Column(Boolean, default=False)

    unidad = relationship("Unidad", back_populates="servicios")
    usuario_levanta = relationship("Usuario", foreign_keys=[usuario_id_levanta], back_populates="servicios_levantados")
    usuario_aprueba = relationship("Usuario", foreign_keys=[usuario_id_aprueba], back_populates="servicios_aprobados")

    pendientes = relationship("ServicioPendiente", back_populates="servicio")
    fallas = relationship("ServicioFalla", back_populates="servicio")
    piezas = relationship("ServicioPieza", back_populates="servicio")
    historial = relationship("ServicioHistorial", back_populates="servicio")
    evidencias = relationship("ServicioEvidencia", back_populates="servicio")
    tiempos = relationship("ServicioTiempo", back_populates="servicio")
    extensiones = relationship("ServicioExtension", back_populates="servicio")
