from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoDiscoEnum(enum.Enum):
    SSD = "SSD"
    HDD = "HDD"
    OTRO = "OTRO"

class DiscoDuro(Base):
    __tablename__ = "discos_duros"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoDiscoEnum), nullable=False)

    # Relación polimórfica viewonly con Pieza
   
    piezas = relationship(
        "Pieza",
        primaryjoin="and_(DiscoDuro.id==foreign(Pieza.id_opcion), Pieza.tipo=='DISCO_DURO')",
        viewonly=True
    )