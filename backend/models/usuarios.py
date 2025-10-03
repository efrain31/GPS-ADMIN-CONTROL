from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20))
    email = Column(String(150), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    activo = Column(Boolean, default=True)
    ultimo_login = Column(TIMESTAMP, nullable=True)

    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    rol = relationship("Rol", back_populates="usuarios")

    unidad_id = Column(Integer, ForeignKey("unidades.id", ondelete="CASCADE"), nullable=True)
    unidad = relationship("Unidad", back_populates="registros")

    servicios_levantados = relationship(
        "Servicio",
        foreign_keys="[Servicio.usuario_id_levanta]",
        back_populates="usuario_levanta"
    )
    servicios_aprobados = relationship(
        "Servicio",
        foreign_keys="[Servicio.usuario_id_aprueba]",
        back_populates="usuario_aprueba"
    )
    servicio_historial = relationship("ServicioHistorial", back_populates="usuario")
    tiempos_servicios = relationship("ServicioTiempo", back_populates="usuario")
    extensiones_servicios = relationship("ServicioExtension", back_populates="usuario")

    piezas_registro = relationship("UnidadPiezaRegistro", back_populates="usuario")

    pendientes_asignados = relationship(
        "ServicioPendiente",
        foreign_keys="[ServicioPendiente.usuario_id_admin]",
        back_populates="usuario_admin"
    )
    pendientes_tecnico = relationship(
        "ServicioPendiente",
        foreign_keys="[ServicioPendiente.tecnico_id]",
        back_populates="tecnico"
    )

    notificaciones = relationship("Notificacion", back_populates="usuario")
