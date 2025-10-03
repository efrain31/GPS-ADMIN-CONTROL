from pydantic import BaseModel
from typing import Optional

class ServicioEvidenciaBase(BaseModel):
    servicio_id: int
    evidencia_id: int
    tipo: Optional[str] = None

class ServicioEvidenciaCreate(ServicioEvidenciaBase):
    pass

class ServicioEvidenciaRead(ServicioEvidenciaBase):
    
    
    
    model_config = {
    "from_attributes": True
}


# ----------  relaciones ----------
class ServicioEvidenciaReadWithRelations(ServicioEvidenciaRead):
    servicio: Optional[int] = None   
    evidencia: Optional[int] = None   
