from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models.usuarios import Usuario
from utils.auth import verify_password, create_access_token, decode_access_token
from sqlalchemy import func

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2 esquema para Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrecta")
    
    # Crea token JWT
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": db_user.email, "id": db_user.id}, 
        expires_delta=access_token_expires
    )
    
    # Guarda último login
    db_user.ultimo_login = func.now()
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "nombre": db_user.nombre,
            "email": db_user.email,
            "rol_id": db_user.rol_id,
            "rol_nombre": db_user.rol.nombre if db_user.rol else None
        }
    }


@router.get("/me")
def get_current_user_info(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    usuario_id = payload.get("id")
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol_id": usuario.rol_id,
        "rol_nombre": usuario.rol.nombre if usuario.rol else None,
        "ultimo_login": usuario.ultimo_login
    }
