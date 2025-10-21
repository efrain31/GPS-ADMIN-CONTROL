from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class EstadoCableEnum(enum.Enum):
    NUEVO = "NUEVO"
    USADO = "USADO"
    DANADO = "DANADO"

class Cable(Base):
    __tablename__ = "cables"

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(Enum(EstadoCableEnum), nullable=False)

    # Relación polimórfica viewonly con Pieza
    piezas = relationship(
        "Pieza",
        primaryjoin="and_(Cable.id==foreign(Pieza.id_opcion), Pieza.tipo=='CABLE')",
        viewonly=True
    )