from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class GpsModelo(Base):
    __tablename__ = "gps_modelos"
    __table_args__ = {"extend_existing": True}  

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(100))
    nodeos = Column(String(50))           # FMDC, FMU, FMC003
    tipo_telefonia = Column(String(50))  
    opcion_cantbus = Column(String(50))
    activo = Column(Boolean, default=True)
    danado = Column(Boolean, default=False)
    motivo_retiro = Column(String(200))
