from typing import Any

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.core.entity.transaction import TransactionBuilder
from wallet.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
    WalletServiceDependable,
)

transactions_api = APIRouter()


class TransactionResponse(BaseModel):
    id: str
    from_address: str
    to_address: str
    amount: int
    fee: int


class TransactionListResponse(BaseModel):
    transaction_list: list[TransactionResponse]


class MakeTransactionRequest(BaseModel):
    sender_wallet_address: str
    receiver_wallet_address: str
    amount: int


@transactions_api.get("/", status_code=201, response_model=TransactionListResponse)
def list_transactions(
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    transaction_service: TransactionServiceDependable,
    api_key: str = Header(..., convert_underscores=False, alias="X-API-KEY"),
) -> dict[str, list[dict[str, Any]]] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(api_key)
        wallets = wallet_service.get_user_wallets(user)
        transactions = [
            transaction
            for wallet in wallets
            for transaction in transaction_service.filter_transactions(wallet)
        ]

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

        return {"transaction_list": response}
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )


@transactions_api.post("/", status_code=201, response_model=None)
def make_transaction(
    make_transaction_request: MakeTransactionRequest,
    user_service: UserServiceDependable,
    transaction_service: TransactionServiceDependable,
    api_key: str = Header(..., convert_underscores=False, alias="X-API-KEY"),
) -> None | JSONResponse:
    try:
        issuer = user_service.get_user_by_api_key(api_key)
        transaction = (
            TransactionBuilder()
            .builder()
            .from_address(make_transaction_request.sender_wallet_address)
            .to_address(make_transaction_request.receiver_wallet_address)
            .amount(make_transaction_request.amount)
            .build()
        )
        transaction_service.create_transaction(transaction, issuer)
        return None
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
