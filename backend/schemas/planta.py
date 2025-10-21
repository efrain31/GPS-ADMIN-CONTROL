from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .unidad import UnidadRead

class PlantaBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None

class PlantaCreate(PlantaBase):
    pass

class PlantaRead(PlantaBase):
    id: int
    model_config = {"from_attributes": True}

class PlantaReadWithUnidades(PlantaRead):
    unidades: Optional[List["UnidadRead"]] = None

# --- Resolver forward references ---
if TYPE_CHECKING is False:
    from .unidad import UnidadRead
    PlantaReadWithUnidades.model_rebuild()
