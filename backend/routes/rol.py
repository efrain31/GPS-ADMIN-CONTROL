from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.roles import Rol
from schemas.rol import RolCreate, RolReadWithRelations
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user 
from models.usuarios import Usuario

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RolReadWithRelations])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@router.post("/", response_model=RolReadWithRelations)
def create_rol(
    rol: RolCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="Solo SuperAdmin puede crear roles")

    nuevo_rol = Rol(**rol.dict())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Nuevo rol {nuevo_rol.nombre} creado",
        tipo="rol",
        referencia_id=nuevo_rol.id
    )
    return nuevo_rol

# --- Actualizar rol (solo SuperAdmin) ---
@router.put("/{rol_id}", response_model=RolReadWithRelations)
def update_rol(
    rol_id: int,
    rol_update: RolCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="Solo SuperAdmin puede actualizar roles")

    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    for key, value in rol_update.dict().items():
        setattr(rol, key, value)
    db.commit()
    db.refresh(rol)
    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Rol {rol.nombre} actualizado",
        tipo="rol",
        referencia_id=rol.id
    )
    return rol

@router.delete("/{rol_id}")
def delete_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="Solo SuperAdmin puede eliminar roles")

    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Rol {rol.nombre} eliminado",
        tipo="rol",
        referencia_id=rol.id
    )
    db.delete(rol)
    db.commit()
    return {"message": "Rol eliminado correctamente"}

