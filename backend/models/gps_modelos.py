from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class NodeosEnum(enum.Enum):
    FMDC = "FMDC"
    FMU = "FMU"
    FMC003 = "FMC003"

class TipoTelefoniaEnum(enum.Enum):
    GSM = "GSM"
    CDMA = "CDMA"
    LTE = "LTE"

class GpsModelo(Base):
    __tablename__ = "gps_modelos"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(100), nullable=False)
    nodeos = Column(Enum(NodeosEnum), nullable=False)
    tipo_telefonia = Column(Enum(TipoTelefoniaEnum), nullable=False)
    opcion_cantbus = Column(String(50), nullable=True)
    activo = Column(Boolean, default=True)
    danado = Column(Boolean, default=False)
    motivo_retiro = Column(String(200), nullable=True)

    # Relación polimórfica con Pieza
    piezas = relationship(
        "Pieza",
        primaryjoin="and_(GpsModelo.id==foreign(Pieza.id_opcion), Pieza.tipo=='GPS')",
        viewonly=True
    )