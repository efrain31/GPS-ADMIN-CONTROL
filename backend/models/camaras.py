from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Camara(Base):
    __tablename__ = "camaras"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)  # FIJA, MOVIL
    ubicacion = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    danado = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("tipo IN ('FIJA', 'MOVIL')", name="chk_tipo_camara"),
    )

    # Relación polimórfica viewonly con Pieza
    piezas = relationship(
        "Pieza",
        primaryjoin="and_(Camara.id==foreign(Pieza.id_opcion), Pieza.tipo=='CAMARA')",
        viewonly=True
    )