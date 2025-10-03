from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from .usuario import UsuarioRead

if TYPE_CHECKING:
    from .usuario import UsuarioRead  

class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass  

class RolRead(RolBase):
    id: int
    
    model_config = {
    "from_attributes": True
}
 

# ---------- relaciones ----------
class RolReadWithRelations(RolRead):
    usuarios: Optional[List["UsuarioRead"]] = [] 

RolReadWithRelations.model_rebuild()
