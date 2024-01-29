from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.core.entity.wallet import WalletBuilder
from wallet.core.tool.converter import Converter, DEFAULT_WALLET_BALANCE
from wallet.infra.fastapi.dependables import WalletServiceDependable, UserServiceDependable

wallet_api = APIRouter()


class WalletResponse(BaseModel):
    address: str
    amount_in_btc: float
    amount_in_usd: float


class WalletRequest(BaseModel):
    api_key: str


@wallet_api.post(path="/", status_code=201, response_model=WalletResponse)
def create_wallet(request: WalletRequest, wallet_service: WalletServiceDependable,
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

    converter = Converter()
    amount_btc = Converter.satoshi_to_btc(wallet.amount)
    amount_usd = converter.btc_to_usd(amount_btc)

    return {"address": wallet.address, "amount_in_btc": amount_btc, "amount_in_usd": amount_usd}


@wallet_api.get(path="/{address}", status_code=200, response_model=WalletResponse)
def get_wallet(address: str, request: WalletRequest, wallet_service: WalletServiceDependable,
               user_service: UserServiceDependable) -> dict[str, Any] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(request.api_key)
        wallet = wallet_service.get_wallet(address, user)
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
    converter = Converter()
    amount_btc = Converter.satoshi_to_btc(wallet.amount)
    amount_usd = converter.btc_to_usd(amount_btc)

    return {"address": wallet.address, "amount_in_btc": amount_btc, "amount_in_usd": amount_usd}
