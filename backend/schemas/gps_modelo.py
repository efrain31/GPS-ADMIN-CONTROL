from pydantic import BaseModel
from typing import Optional

class GpsModeloBase(BaseModel):
    modelo: str
    nodeos: Optional[str] = None
    tipo_telefonia: Optional[str] = None
    opcion_cantbus: Optional[str] = None
    activo: Optional[bool] = True
    danado: Optional[bool] = False
    motivo_retiro: Optional[str] = None

class GpsModeloCreate(GpsModeloBase):
    pass

class GpsModeloRead(GpsModeloBase):
    id: int

    model_config = {
    "from_attributes": True
}

