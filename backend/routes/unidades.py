from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.unidades import Unidad
from schemas.unidad import UnidadCreate, UnidadReadWithRelations
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/unidades", tags=["Unidades"])

# -------------------- Mapper --------------------
def map_unidad(unidad: Unidad) -> UnidadReadWithRelations:
    return UnidadReadWithRelations(
        id=unidad.id,
        empresa=unidad.empresa,  # carga solo la empresa
        tipo=unidad.tipo,
        caracteristicas=unidad.caracteristicas,
        ignicion_movimiento=unidad.ignicion_movimiento,
        inventario=[],      # si no quieres cargar relaciones, dejarlas vacías
        logs_fallas=[],
        servicios=[]
    )

# -------------------- Endpoints --------------------

# Select unidades (id + tipo)
@router.get("/selectunidad", response_model=List[dict])
def select_unidades(db: Session = Depends(get_db)):
    unidades = db.query(Unidad.id, Unidad.tipo).all()
    return [{"id": u.id, "tipo": u.tipo} for u in unidades]

# Listar todas las unidades con empresa
@router.get("/all", response_model=List[UnidadReadWithRelations])
def get_unidades(db: Session = Depends(get_db)):
    unidades = db.query(Unidad).all()
    return [map_unidad(u) for u in unidades]

# Crear unidad
@router.post("/crear", response_model=UnidadReadWithRelations)
def create_unidad(
    unidad: UnidadCreate, 
    db: Session = Depends(get_db), 
    usuario = Depends(get_current_user)
):
    nueva = Unidad(**unidad.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    crear_notificacion(
        db, 
        usuario_id=usuario.id, 
        mensaje=f"Unidad {nueva.tipo} creada", 
        tipo="unidad", 
        referencia_id=nueva.id
    )
    return map_unidad(nueva)

# Actualizar unidad
@router.put("/actualizar/{unidad_id}", response_model=UnidadReadWithRelations)
def update_unidad(
    unidad_id: int, 
    unidad_update: UnidadCreate, 
    db: Session = Depends(get_db), 
    usuario = Depends(get_current_user)
):
    unidad = db.get(Unidad, unidad_id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    for key, value in unidad_update.dict().items():
        setattr(unidad, key, value)
    db.commit()
    db.refresh(unidad)
    crear_notificacion(
        db, 
        usuario_id=usuario.id, 
        mensaje=f"Unidad {unidad.tipo} actualizada", 
        tipo="unidad", 
        referencia_id=unidad.id
    )
    return map_unidad(unidad)

# Borrar unidad
@router.delete("/borrar/{unidad_id}")
def delete_unidad(
    unidad_id: int, 
    db: Session = Depends(get_db), 
    usuario = Depends(get_current_user)
):
    unidad = db.get(Unidad, unidad_id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    crear_notificacion(
        db, 
        usuario_id=usuario.id, 
        mensaje=f"Unidad {unidad.tipo} eliminada", 
        tipo="unidad", 
        referencia_id=unidad.id
    )
    db.delete(unidad)
    db.commit()
    return {"message": "Unidad eliminada correctamente"}
