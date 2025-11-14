from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import CalcResult
from src.schemas.calc_schemas import CalcRequest
from src.utils.setup_logger import logger


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = CalcResult

    @logger
    async def calculate_and_save(self, data: CalcRequest) -> float:
        total = sum(m.qty * m.price_rub for m in data.materials)
        result = CalcResult(total_cost_rub=total)
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return float(result.total_cost_rub)

    @logger
    async def get_last_calculations(self, limit: int = 10):
        stmt = select(CalcResult).order_by(desc(CalcResult.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
