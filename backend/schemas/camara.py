from pydantic import BaseModel
from typing import Optional, List

# ---------- Base ----------
class CamaraBase(BaseModel):
    tipo: str
    ubicacion: Optional[str] = None
    activo: Optional[bool] = True
    danado: Optional[bool] = False

# ---------- Crear ----------
class CamaraCreate(CamaraBase):
    pass

# ---------- Leer ----------
class CamaraRead(CamaraBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ---------- Leer con relaciones ----------
class CamaraReadWithRelations(CamaraRead):
    piezas: Optional[List[int]] = []
