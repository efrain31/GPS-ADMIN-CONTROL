from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionRead(BaseModel):
    id: int
    usuario_id: int
    mensaje: str
    tipo: Optional[str] = None
    referencia_id: Optional[int] = None
    leida: Optional[bool] = False
    fecha: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
