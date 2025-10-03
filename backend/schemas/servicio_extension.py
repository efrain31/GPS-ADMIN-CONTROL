from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .usuario import UsuarioRead
from .servicio import ServicioRead

class ServicioExtensionBase(BaseModel):
    servicio_id: int
    usuario_id: int
    duracion: Optional[str] = None
    fecha_solicitud: Optional[datetime] = None
    aprobado: Optional[bool] = False

class ServicioExtensionCreate(ServicioExtensionBase):
    pass

class ServicioExtensionRead(ServicioExtensionBase):
    id: int
    
    

    model_config = {
    "from_attributes": True
}


# ----------  relaciones  ----------
class ServicioExtensionReadWithRelations(ServicioExtensionRead):
    servicio: Optional[ServicioRead] = None
    usuario: Optional[UsuarioRead] = None
