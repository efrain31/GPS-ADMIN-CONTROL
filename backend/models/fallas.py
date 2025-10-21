from sqlalchemy import Column, Integer, Text, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Falla(Base):
    __tablename__ = "fallas"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)

    # Validación para que la descripción no esté vacía
    __table_args__ = (
        CheckConstraint("descripcion <> ''", name="chk_descripcion_no_vacia"),
    )

    # Relaciones
    logs = relationship("LogFalla", back_populates="falla")
    servicios = relationship("ServicioFalla", back_populates="falla")
