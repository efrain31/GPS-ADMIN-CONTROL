from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from .notificacione import NotificacionRead
from .servicio_pendiente import ServicioPendienteRead

# --- Base ---
class UsuarioBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: EmailStr
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    password: str
    
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None
    rol_id: Optional[int] = None

class UsuarioRead(UsuarioBase):
    id: int
    ultimo_login: Optional[datetime] = None
    rol_id: Optional[int] = None

    class Config:
        from_attributes = True

class UsuarioReadWithRelations(UsuarioRead):
    servicios_levantados: Optional[List[int]] = []  
    servicios_aprobados: Optional[List[int]] = []
    servicio_historial: Optional[List[int]] = []
    servicio_tiempo: Optional[List[int]] = []
    servicio_extension: Optional[List[int]] = []

    notificaciones: List[NotificacionRead] = Field(default_factory=list)
    pendientes_asignados: List[ServicioPendienteRead] = Field(default_factory=list)
    pendientes_tecnico: List[ServicioPendienteRead] = Field(default_factory=list)

# --- Login / Auth ---
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
