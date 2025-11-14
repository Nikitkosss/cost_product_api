from datetime import datetime
from sqlalchemy import (
    Column,
    Numeric,
    DateTime,
    Integer,
)

from src.db.database import Base


class CalcResult(Base):
    __tablename__ = "calc_results"

    id = Column(Integer, primary_key=True, index=True)
    total_cost_rub = Column(Numeric(precision=15, scale=2))
    created_at = Column(DateTime, default=datetime.utcnow)
