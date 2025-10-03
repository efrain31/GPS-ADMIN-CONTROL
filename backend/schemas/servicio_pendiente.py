from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServicioPendienteBase(BaseModel):
    servicio_id: int
    usuario_id_admin: Optional[int] = None
    tecnico_id: Optional[int] = None
    estado: Optional[str] = None
    fecha_registro: Optional[datetime] = None

class ServicioPendienteCreate(ServicioPendienteBase):
    pass

class ServicioPendienteRead(ServicioPendienteBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class ServicioPendienteReadWithRelations(ServicioPendienteRead):
    servicio: Optional[int] = None       
    usuario_admin: Optional[int] = None  
    tecnico: Optional[int] = None        
