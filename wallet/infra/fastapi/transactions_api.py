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


class ApiRequest(BaseModel):
    api_key: str


class MakeTransactionRequest(BaseModel):
    api_key: str
    sender_wallet_address: str
    receiver_wallet_address: str
    amount: int


@transactions_api.get("/", status_code=201, response_model=TransactionListResponse)
def list_transactions(
    list_request: ApiRequest,
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    transaction_service: TransactionServiceDependable,
) -> list[Transaction] | JSONResponse:
    try:
        user = user_service.get_user_by_api_key(list_request.api_key)
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


@transactions_api.post("/", status_code=201, response_model=None)
def make_transaction(
    make_transaction_request: MakeTransactionRequest,
    user_service: UserServiceDependable,
    transaction_service: TransactionServiceDependable,
) -> None | JSONResponse:
    try:
        issuer = user_service.get_user_by_api_key(make_transaction_request.api_key)
        transaction = (
            TransactionBuilder()
            .builder()
            .from_address(make_transaction_request.sender_wallet_address)
            .to_address(make_transaction_request.receiver_wallet_address)
            .amount(make_transaction_request.amount)
            .build()
        )
        transaction_service.create_transaction(transaction, issuer)
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
