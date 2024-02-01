from fastapi import FastAPI

from wallet.core.facade import TransactionService, UserService, WalletService
from wallet.infra.fastapi.users_api import users_api
from wallet.infra.fastapi.wallets_api import wallet_api
from wallet.infra.fastapi.transactions_api import transactions_api 
from wallet.infra.repository.memory.transaction_repository import TransactionRepository
from wallet.infra.repository.memory.wallet_repository import WalletRepository
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.user_repository import UserRepository


def setup() -> FastAPI:
    api = FastAPI()
    api.include_router(users_api, prefix="/users")
    api.include_router(wallet_api, prefix="/wallets")
    api.include_router(transactions_api, prefix="/transactions")

    api.state.user_service = UserService(UserRepository())
    api.state.wallet_service = WalletService(WalletRepository())
    api.state.transaction_service = TransactionService(
        TransactionRepository(), WalletRepository()
    )
    return api


def destroy() -> None:
    ConnectionManager.close_all()
