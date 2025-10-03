from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServicioHistorialBase(BaseModel):
    servicio_id: int
    usuario_id: int
    accion: Optional[str] = None
    fecha: Optional[datetime] = None

class ServicioHistorialCreate(ServicioHistorialBase):
    pass

class ServicioHistorialRead(ServicioHistorialBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class ServicioHistorialReadWithRelations(ServicioHistorialRead):
    servicio: Optional[int] = None 
    usuario: Optional[int] = None  

