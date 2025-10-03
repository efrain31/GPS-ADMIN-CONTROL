from sqlalchemy.orm import Session
from models.notificaciones import Notificacion

def crear_notificacion(db: Session, usuario_id: int, mensaje: str, tipo: str, referencia_id: int):
    noti = Notificacion(
        usuario_id=usuario_id,
        mensaje=mensaje,
        tipo=tipo,
        referencia_id=referencia_id
    )
    db.add(noti)
    db.commit()
