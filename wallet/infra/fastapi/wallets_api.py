from typing import Any

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.core.entity.wallet import WalletBuilder
from wallet.core.tool.converter import DEFAULT_WALLET_BALANCE, Converter
from wallet.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
    WalletServiceDependable,
)

wallet_api = APIRouter()


class WalletResponse(BaseModel):
    address: str
    amount_in_btc: float
    amount_in_usd: float


class WalletTransactionResponse(BaseModel):
    id: str
    from_address: str
    to_address: str
    amount: int
    fee: int


class WalletTransactionsResponse(BaseModel):
    transactions: list[WalletTransactionResponse]


@wallet_api.post(path="/", status_code=201, response_model=WalletResponse)
def create_wallet(
    wallet_service: WalletServiceDependable,
    user_service: UserServiceDependable,
    api_key: str = Header(..., convert_underscores=False),
) -> dict[str, Any] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(api_key)
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )

    wallet = (
        WalletBuilder()
        .builder()
        .user_id(user.user_id)
        .amount(DEFAULT_WALLET_BALANCE)
        .build()
    )
    wallet = wallet_service.create_wallet(wallet)

    converter = Converter()
    amount_btc = Converter.satoshi_to_btc(wallet.amount)
    amount_usd = converter.btc_to_usd(amount_btc)

    return {
        "address": wallet.address,
        "amount_in_btc": amount_btc,
        "amount_in_usd": amount_usd,
    }


@wallet_api.get(path="/{address}", status_code=200, response_model=WalletResponse)
def get_wallet(
    address: str,
    wallet_service: WalletServiceDependable,
    user_service: UserServiceDependable,
    api_key: str = Header(..., convert_underscores=False),
) -> dict[str, Any] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(api_key)
        wallet = wallet_service.get_wallet(address, user)
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
    converter = Converter()
    amount_btc = Converter.satoshi_to_btc(wallet.amount)
    amount_usd = converter.btc_to_usd(amount_btc)

    return {
        "address": wallet.address,
        "amount_in_btc": amount_btc,
        "amount_in_usd": amount_usd,
    }


@wallet_api.get(
    path="/{address}/transactions",
    status_code=200,
    response_model=WalletTransactionsResponse,
)
def get_wallet_transactions(
    address: str,
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    transaction_service: TransactionServiceDependable,
    api_key: str = Header(..., convert_underscores=False),
) -> dict[str, Any] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(api_key)
        wallet = wallet_service.get_wallet(address, user)
        transactions = transaction_service.filter_transactions(wallet)
        response = [
            {
                "id": str(t.transaction_id),
                "from_address": t.from_address,
                "to_address": t.to_address,
                "amount": t.amount,
                "fee": t.fee,
            }
            for t in set(transactions)
        ]
        return {"transactions": response}
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
