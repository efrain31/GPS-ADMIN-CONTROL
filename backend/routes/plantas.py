from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.planta import Planta
from schemas.planta import PlantaCreate, PlantaRead

router = APIRouter(prefix="/plantas", tags=["Plantas"])

# Listar todas las plantas (para select)
@router.get("/select", response_model=List[dict])
def select_plantas(db: Session = Depends(get_db)):
    plantas = db.query(Planta.id, Planta.nombre).all()
    return [{"id": p.id, "nombre": p.nombre} for p in plantas]

# Listar todas las plantas con detalle
@router.get("/all", response_model=List[PlantaRead])
def get_plantas(db: Session = Depends(get_db)):
    return db.query(Planta).all()

# Crear planta
@router.post("/crear", response_model=PlantaRead)
def create_planta(planta: PlantaCreate, db: Session = Depends(get_db)):
    nueva = Planta(**planta.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


