from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.core.entity.wallet import WalletBuilder, DEFAULT_WALLET_BALANCE, BTC_TO_SATOSHI
from wallet.core.error.errors import DoesNotExistError
from wallet.infra.fastapi.dependables import WalletServiceDependable, UserServiceDependable


wallet_api = APIRouter()


class CreateWalletResponse(BaseModel):
    address: str
    amount_in_btc: float
    amount_in_usd: float


class CreateWalletRequest(BaseModel):
    api_key: str


@wallet_api.post(path="/", status_code=201, response_model=CreateWalletResponse)
def create_wallet(request: CreateWalletRequest, wallet_service: WalletServiceDependable,
                  user_service: UserServiceDependable) -> dict[str, Any] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(request.api_key)
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )

    wallet = WalletBuilder().builder().user_id(user.user_id).amount(DEFAULT_WALLET_BALANCE).build()
    wallet = wallet_service.create_wallet(wallet)

    return {"address": wallet.address, "amount_in_btc": 1, "amount_in_usd": 1}
