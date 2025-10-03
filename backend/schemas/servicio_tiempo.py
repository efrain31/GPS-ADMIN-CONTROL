from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .usuario import UsuarioRead
from .servicio import ServicioRead

class ServicioTiempoBase(BaseModel):
    servicio_id: int
    usuario_id: int
    accion: Optional[str] = None
    timestamp: Optional[datetime] = None

class ServicioTiempoCreate(ServicioTiempoBase):
    pass

class ServicioTiempoRead(ServicioTiempoBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class ServicioTiempoReadWithRelations(ServicioTiempoRead):
    servicio: Optional[ServicioRead] = None
    usuario: Optional[UsuarioRead] = None
