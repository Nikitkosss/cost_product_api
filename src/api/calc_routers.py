from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.schemas.calc_schemas import CalcRequest, CalcResponse
from src.services.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/product", tags=["Продукт"])


@router.post("/calc", response_model=CalcResponse, summary="Расчёта стоимости изделия")
async def calculate_and_save(data: CalcRequest, uow: UnitOfWork = Depends(get_uow)):
    total = await uow.calc_service.calculate_and_save(data=data)
    return {"total_cost_rub": total}


@router.get(
    "/calc",
    summary="Возвращает 10 последних расчётов отсортированных по дате",
)
async def get_last_calculations(
    limit: Optional[int] = Query(default=10, ge=0), uow: UnitOfWork = Depends(get_uow)
):
    return await uow.calc_service.get_last_calculations(limit=limit)
