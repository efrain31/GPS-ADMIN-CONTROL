from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoLectoraEnum(enum.Enum):
    CODIGO = "CODIGO"
    BARRAS = "BARRAS"
    RFID = "RFID"
class Lectora(Base):
    __tablename__ = "lectoras"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoLectoraEnum), nullable=False)

    # Relación polimórfica viewonly
    piezas = relationship(
        "Pieza",
        primaryjoin="and_(Lectora.id==foreign(Pieza.id_opcion), Pieza.tipo=='LECTORA')",
        viewonly=True
    )