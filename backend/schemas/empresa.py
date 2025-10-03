from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .unidad import UnidadRead 

class EmpresaBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaRead(EmpresaBase):
    id: int

    model_config = {
    "from_attributes": True
}


# ---------- Con relación a unidades ----------
class EmpresaReadWithUnidades(EmpresaRead):
    unidades: Optional[List["UnidadRead"]] = []  

from .unidad import UnidadRead
EmpresaReadWithUnidades.model_rebuild()
