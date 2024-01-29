from fastapi import FastAPI

from wallet.core.facade import UserService, WalletService
from wallet.infra.fastapi.users_api import users_api
from wallet.infra.fastapi.wallets_api import wallet_api
from wallet.infra.repository.memory.wallet_repository import WalletRepository
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.user_repository import UserRepository


def setup() -> FastAPI:
    api = FastAPI()
    api.include_router(users_api, prefix="/users")
    api.include_router(wallet_api, prefix="/wallets")

    api.state.user_service = UserService(UserRepository())
    api.state.wallet_service = WalletService(WalletRepository())
    return api


def destroy() -> None:
    ConnectionManager.close_all()
