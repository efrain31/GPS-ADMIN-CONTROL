from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from database import get_db
from models.empresas import Empresa
from schemas.empresa import EmpresaCreate, EmpresaReadWithUnidades
from utils.notificaciones import crear_notificacion

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.get("/", response_model=List[EmpresaReadWithUnidades])
def get_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@router.post("/", response_model=EmpresaReadWithUnidades)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    nueva_empresa = Empresa(**empresa.dict())
    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)
    crear_notificacion(db, usuario_id=1, mensaje=f"Empresa {nueva_empresa.nombre} creada", tipo="empresa", referencia_id=nueva_empresa.id)
    return nueva_empresa

@router.put("/{empresa_id}", response_model=EmpresaReadWithUnidades)
def update_empresa(empresa_id: int, empresa_update: EmpresaCreate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    for key, value in empresa_update.dict().items():
        setattr(empresa, key, value)
    db.commit()
    db.refresh(empresa)
    crear_notificacion(db, usuario_id=1, mensaje=f"Empresa {empresa.nombre} actualizada", tipo="empresa", referencia_id=empresa.id)
    return empresa

@router.delete("/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    crear_notificacion(db, usuario_id=1, mensaje=f"Empresa {empresa.nombre} eliminada", tipo="empresa", referencia_id=empresa.id)
    db.delete(empresa)
    db.commit()
    return {"message": "Empresa eliminada correctamente"}

@router.get("/select", response_model=List[Dict[str, str]])
def get_empresas_select(db: Session = Depends(get_db)):
    empresas = db.query(Empresa.id, Empresa.nombre).all()
    return [{"id": str(e.id), "nombre": e.nombre} for e in empresas]
