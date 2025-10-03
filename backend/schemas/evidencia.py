from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .servicio_evidencia import ServicioEvidenciaReadWithRelations

class EvidenciaBase(BaseModel):
    url_imagen: Optional[str] = None
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None

class EvidenciaCreate(EvidenciaBase):
    pass

class EvidenciaRead(EvidenciaBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ----------  relaciones  ----------
class EvidenciaReadWithRelations(EvidenciaRead):
    servicios: Optional[List[ServicioEvidenciaReadWithRelations]] = []

