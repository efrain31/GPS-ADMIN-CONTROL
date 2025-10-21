from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

class ServicioBase(BaseModel):
    usuario_id_levanta: Optional[int] = None
    usuario_id_aprueba: Optional[int] = None
    unidad_id: Optional[int] = None
    planta_id: Optional[int] = None  
    cambios: Optional[str] = None
    items: Optional[str] = None
    comentarios: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_liberacion: Optional[date] = None
    estado: Optional[str] = None
    domiciliado: Optional[bool] = False
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    pendiente: Optional[bool] = False
    reasignado_admin: Optional[bool] = False


class ServicioUpdate(BaseModel):
    usuario_id_levanta: Optional[int] = None
    usuario_id_aprueba: Optional[int] = None
    unidad_id: Optional[int] = None
    cambios: Optional[str] = None
    items: Optional[str] = None
    comentarios: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_liberacion: Optional[date] = None
    estado: Optional[str] = None
    domiciliado: Optional[bool] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    pendiente: Optional[bool] = None
    reasignado_admin: Optional[bool] = None

    class Config:
        orm_mode = True

class ServicioCreate(ServicioBase):
    pass

class ServicioRead(ServicioBase):
    id: int


# ----------  relaciones ----------
class ServicioReadWithRelations(ServicioRead):
    unidad: Optional[int] = None  
    unidad_nombre: Optional[str] = None         
    usuario_levanta: Optional[int] = None 
    usuario_levanta_nombre: Optional[str] = None 
    usuario_aprueba: Optional[int] = None  
    usuario_aprueba_nombre: Optional[str] = None
    planta: Optional[str] = None 
    pendientes: Optional[List[int]] = []   
    fallas: Optional[List[int]] = []        
    piezas: Optional[List[int]] = []       
    historial: Optional[List[int]] = []    
    evidencias: Optional[List[int]] = []   
    tiempos: Optional[List[int]] = []      
    extensiones: Optional[List[int]] = []  
    
    
    model_config = {
    "from_attributes": True
}