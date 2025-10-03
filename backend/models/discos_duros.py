from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base

class DiscoDuro(Base):
    __tablename__ = "discos_duros"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50))

    __table_args__ = (
        CheckConstraint("tipo IN ('SSD', 'HDD', 'OTRO')", name="chk_tipo_disco"),
    )
