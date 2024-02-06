from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.infra.fastapi.dependables import TransactionServiceDependable

statistics_api = APIRouter()

admin_api_key: str = "f215d09f570b2799c8adb1eb97df6d67ac2578ca7eee2ad200e336958b9d1bef"


class StatisticsResponse(BaseModel):
    transaction_count: int
    profit: int


@statistics_api.get("/", status_code=201, response_model=StatisticsResponse)
def list_transactions(
    transaction_service: TransactionServiceDependable,
    api_key: str = Header(..., convert_underscores=False, alias="X-API-KEY"),
) -> dict[str, int] | JSONResponse:
    if api_key != admin_api_key:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    transaction_count: int = transaction_service.get_transaction_count()
    profit: int = transaction_service.get_profit()
    return {"transaction_count": transaction_count, "profit": profit}
