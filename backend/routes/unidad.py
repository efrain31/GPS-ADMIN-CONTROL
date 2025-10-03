from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.unidades import Unidad
from schemas.unidad import UnidadCreate, UnidadReadWithRelations
from utils.notificaciones import crear_notificacion

router = APIRouter(prefix="/unidades", tags=["Unidades"])

@router.get("/", response_model=List[UnidadReadWithRelations])
def get_unidades(db: Session = Depends(get_db)):
    return db.query(Unidad).all()

@router.post("/", response_model=UnidadReadWithRelations)
def create_unidad(unidad: UnidadCreate, db: Session = Depends(get_db)):
    nueva_unidad = Unidad(**unidad.dict())
    db.add(nueva_unidad)
    db.commit()
    db.refresh(nueva_unidad)
    crear_notificacion(db, usuario_id=1, mensaje=f"Unidad {nueva_unidad.tipo} creada", tipo="unidad", referencia_id=nueva_unidad.id)
    return nueva_unidad

@router.put("/{unidad_id}", response_model=UnidadReadWithRelations)
def update_unidad(unidad_id: int, unidad_update: UnidadCreate, db: Session = Depends(get_db)):
    unidad = db.query(Unidad).filter(Unidad.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    for key, value in unidad_update.dict().items():
        setattr(unidad, key, value)
    db.commit()
    db.refresh(unidad)
    crear_notificacion(db, usuario_id=1, mensaje=f"Unidad {unidad.tipo} actualizada", tipo="unidad", referencia_id=unidad.id)
    return unidad

@router.delete("/{unidad_id}")
def delete_unidad(unidad_id: int, db: Session = Depends(get_db)):
    unidad = db.query(Unidad).filter(Unidad.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    crear_notificacion(db, usuario_id=1, mensaje=f"Unidad {unidad.tipo} eliminada", tipo="unidad", referencia_id=unidad.id)
    db.delete(unidad)
    db.commit()
    return {"message": "Unidad eliminada correctamente"}

