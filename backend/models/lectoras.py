from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base

class Lectora(Base):
    __tablename__ = "lectoras"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50))

    __table_args__ = (
        CheckConstraint("tipo IN ('CODIGO', 'BARRAS', 'RFID')", name="chk_tipo_lectora"),
    )
