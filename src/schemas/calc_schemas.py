from typing import List

from src.schemas.extended_base_model import ExtendedBaseModel


class Material(ExtendedBaseModel):
    name: str
    qty: float
    price_rub: float


class CalcRequest(ExtendedBaseModel):
    materials: List[Material]


class CalcResponse(ExtendedBaseModel):
    total_cost_rub: float


class CalcResult(ExtendedBaseModel):
    id: int
    total_cost_rub: float
    created_at: str
