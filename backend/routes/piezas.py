from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.piezas import Pieza
from schemas.pieza import PiezaCreate, PiezaRead, PiezaReadWithRelations

router = APIRouter(prefix="/piezas", tags=["Piezas"])

def map_pieza_relations(pieza: Pieza) -> PiezaReadWithRelations:
    return PiezaReadWithRelations(
        id=pieza.id,
        tipo=pieza.tipo,
        id_opcion=pieza.id_opcion,
        nombre=pieza.nombre,
        descripcion=pieza.descripcion,
        stock=pieza.stock,
        inventario_interno=[i.id for i in pieza.inventario_interno],
        servicio_piezas=[s.pieza_id for s in pieza.servicio_piezas],
    )

@router.get("/", response_model=List[PiezaReadWithRelations])
def get_piezas(db: Session = Depends(get_db)):
    piezas = db.query(Pieza).all()
    return [map_pieza_relations(p) for p in piezas]


@router.get("/{pieza_id}", response_model=PiezaReadWithRelations)
def get_pieza(pieza_id: int, db: Session = Depends(get_db)):
    pieza = db.query(Pieza).filter(Pieza.id == pieza_id).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    return map_pieza_relations(pieza)


@router.post("/", response_model=PiezaReadWithRelations)
def create_pieza(pieza: PiezaCreate, db: Session = Depends(get_db)):
    nueva_pieza = Pieza(**pieza.dict())
    db.add(nueva_pieza)
    db.commit()
    db.refresh(nueva_pieza)
    return map_pieza_relations(nueva_pieza)


@router.put("/{pieza_id}", response_model=PiezaReadWithRelations)
def update_pieza(pieza_id: int, pieza_update: PiezaCreate, db: Session = Depends(get_db)):
    pieza = db.query(Pieza).filter(Pieza.id == pieza_id).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")

    for key, value in pieza_update.dict(exclude_unset=True).items():
        setattr(pieza, key, value)

    db.commit()
    db.refresh(pieza)
    return map_pieza_relations(pieza)

@router.delete("/{pieza_id}")
def delete_pieza(pieza_id: int, db: Session = Depends(get_db)):
    pieza = db.query(Pieza).filter(Pieza.id == pieza_id).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")

    db.delete(pieza)
    db.commit()
    return {"message": "Pieza eliminada correctamente"}


