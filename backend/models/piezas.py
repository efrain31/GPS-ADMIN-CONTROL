from sqlalchemy import Column, Integer, String, Text, Enum, CheckConstraint, UniqueConstraint, and_
from sqlalchemy.orm import relationship, foreign
from database import Base
import enum

class TipoPiezaEnum(str, enum.Enum):
    CAMARA = "CAMARA"
    LECTORA = "LECTORA"
    DISCO_DURO = "DISCO_DURO"
    CABLE = "CABLE"
    GPS = "GPS"

class Pieza(Base):
    __tablename__ = "piezas"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoPiezaEnum), nullable=False)
    id_opcion = Column(Integer, nullable=False)  # id de la tabla específica
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    stock = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        CheckConstraint("stock >= 0", name="chk_stock_no_negativo"),
        UniqueConstraint('tipo', 'id_opcion', name='uq_tipo_id_opcion'),
    )

    # Relaciones con otras tablas
    inventario_interno = relationship("InventarioInterno", back_populates="pieza")
    servicio_piezas = relationship("ServicioPieza", back_populates="pieza")

    # Relaciones polimórficas viewonly usando foreign()
    camara = relationship(
        "Camara",
        primaryjoin="and_(foreign(Pieza.id_opcion)==Camara.id, Pieza.tipo=='CAMARA')",
        viewonly=True
    )
    gps = relationship(
        "GpsModelo",
        primaryjoin="and_(foreign(Pieza.id_opcion)==GpsModelo.id, Pieza.tipo=='GPS')",
        viewonly=True
    )
    lectora = relationship(
        "Lectora",
        primaryjoin="and_(foreign(Pieza.id_opcion)==Lectora.id, Pieza.tipo=='LECTORA')",
        viewonly=True
    )
    disco_duro = relationship(
        "DiscoDuro",
        primaryjoin="and_(foreign(Pieza.id_opcion)==DiscoDuro.id, Pieza.tipo=='DISCO_DURO')",
        viewonly=True
    )
    cable = relationship(
        "Cable",
        primaryjoin="and_(foreign(Pieza.id_opcion)==Cable.id, Pieza.tipo=='CABLE')",
        viewonly=True
    )
