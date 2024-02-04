from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.core.entity.transaction import Transaction, TransactionBuilder
from wallet.infra.fastapi.dependables import (
    UserServiceDependable,
    WalletServiceDependable,
    TransactionServiceDependable,
)

transactions_api = APIRouter()


class TransactionListResponse(BaseModel):
    transactions_list: list

class TransactionIdResponse(BaseModel):
    transaction_id: str


@transactions_api.get("/", status_code=201, response_model=TransactionListResponse)
def list_transactions(
    api_key: str,
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    transaction_service: TransactionServiceDependable,
) -> list[Transaction] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(api_key)
        wallets = wallet_service.get_user_wallets(user)
        transactions: list[Transaction] = []
        for wallet in wallets:
            transactions += transaction_service.filter_transactions(wallet)

        return transactions
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )


@transactions_api.post("/", status_code=201, response_model=TransactionIdResponse)
def make_transaction(
    api_key: str,
    sender_wallet_address: str,
    receiver_wallet_address: str,
    amount: int,
    user_service: UserServiceDependable,
    transaction_service: TransactionServiceDependable,
) -> TransactionIdResponse | JSONResponse:
    try:
        issuer = user_service.get_user_by_api_key(api_key)
        transaction = (
            TransactionBuilder()
            .builder()
            .from_address(sender_wallet_address)
            .to_address(receiver_wallet_address)
            .amount(amount)
            .build()
        )
        return transaction_service.create_transaction(transaction, issuer).transaction_id
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
