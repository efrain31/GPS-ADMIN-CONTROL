from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models.unidad_pieza_registro import UnidadPiezaRegistro
from models.usuarios import Usuario
from schemas.unidad_pieza_registro import UnidadPiezaRegistroCreate, UnidadPiezaRegistroReadWithRelations, UnidadPiezaRegistroUpdate
from schemas.notificacione import NotificacionRead
from utils.notificaciones import crear_notificacion
from utils.deps import get_current_user

router = APIRouter(prefix="/registros", tags=["UnidadPiezaRegistro"])

# --- Mapear relaciones ---
def map_registro_relations(registro: UnidadPiezaRegistro) -> UnidadPiezaRegistroReadWithRelations:
    return UnidadPiezaRegistroReadWithRelations(
        id=registro.id,
        unidad_id=registro.unidad_id,
        inventario_id=registro.inventario_id,
        cantbus=registro.cantbus,
        danado=registro.danado,
        fecha_actualizacion=registro.fecha_actualizacion,
        usuario_id=registro.usuario_id,
        motivo_cambio=registro.motivo_cambio,
        unidad=registro.unidad.nombre if registro.unidad else None,
        inventario=registro.inventario.id if registro.inventario else None,
        usuario=registro.usuario.nombre if registro.usuario else None,
        notificaciones=[NotificacionRead.from_orm(n) for n in getattr(registro, "notificaciones", [])]
    )


# --- Obtener todos los registros ---
@router.get("/", response_model=List[UnidadPiezaRegistroReadWithRelations])
def get_registros(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    registros = db.query(UnidadPiezaRegistro).all()
    return [map_registro_relations(r) for r in registros]

# --- Obtener registro por ID ---
@router.get("/{registro_id}", response_model=UnidadPiezaRegistroReadWithRelations)
def get_registro(registro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    registro = db.query(UnidadPiezaRegistro).filter(UnidadPiezaRegistro.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return map_registro_relations(registro)

# --- Crear registro ---
@router.post("/", response_model=UnidadPiezaRegistroReadWithRelations)
def create_registro(registro: UnidadPiezaRegistroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear registros")

    nuevo_registro = UnidadPiezaRegistro(
        unidad_id=registro.unidad_id,
        inventario_id=registro.inventario_id,
        cantbus=registro.cantbus,
        danado=registro.danado,
        usuario_id=current_user.id,
        motivo_cambio=registro.motivo_cambio,
        fecha_actualizacion=datetime.now()
    )

    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Registro {nuevo_registro.id} creado",
        tipo="registro",
        referencia_id=nuevo_registro.id
    )

    return map_registro_relations(nuevo_registro)

# --- Actualizar registro ---
@router.put("/{registro_id}", response_model=UnidadPiezaRegistroReadWithRelations)
def update_registro(registro_id: int, registro_update: UnidadPiezaRegistroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    registro = db.query(UnidadPiezaRegistro).filter(UnidadPiezaRegistro.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar registros")

    update_data = registro_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(registro, key, value)
    registro.fecha_actualizacion = datetime.now()

    db.commit()
    db.refresh(registro)

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Registro {registro.id} actualizado",
        tipo="registro",
        referencia_id=registro.id
    )

    return map_registro_relations(registro)

# --- Eliminar registro ---
@router.delete("/{registro_id}")
def delete_registro(registro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    registro = db.query(UnidadPiezaRegistro).filter(UnidadPiezaRegistro.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if current_user.rol_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar registros")

    crear_notificacion(
        db,
        usuario_id=current_user.id,
        mensaje=f"Registro {registro.id} eliminado",
        tipo="registro",
        referencia_id=registro.id
    )

    db.delete(registro)
    db.commit()
    return {"message": "Registro eliminado correctamente"}
