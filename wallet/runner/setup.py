from fastapi import FastAPI

from wallet.core.facade import UserService
from wallet.infra.fastapi.users_api import users_api
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.user_repository import UserRepository


def setup() -> FastAPI:
    api = FastAPI()
    api.include_router(users_api, prefix="/users")

    api.state.user_service = UserService(UserRepository())

    return api


def destroy() -> None:
    ConnectionManager.close_all()
