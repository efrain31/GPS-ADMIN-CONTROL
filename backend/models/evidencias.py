from sqlalchemy import Column, Integer, Text, TIMESTAMP, CheckConstraint, func
from sqlalchemy.orm import relationship
from database import Base

class Evidencia(Base):
    __tablename__ = "evidencias"

    id = Column(Integer, primary_key=True, index=True)
    url_imagen = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("url_imagen <> ''", name="chk_url_imagen_no_vacio"),
        CheckConstraint("descripcion <> ''", name="chk_descripcion_no_vacio"),
    )

    servicios = relationship("ServicioEvidencia", back_populates="evidencia")
