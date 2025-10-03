from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base

class Cable(Base):
    __tablename__ = "cables"

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50))

    __table_args__ = (
        CheckConstraint("estado IN ('NUEVO', 'USADO', 'DANADO')", name="chk_estado_cable"),
    )
