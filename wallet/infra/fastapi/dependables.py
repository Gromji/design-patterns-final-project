from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from wallet.core.facade import UserService, WalletService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service  # type: ignore


def get_wallet_service(request: Request) -> WalletService:
    return request.app.state.wallet_service


UserServiceDependable = Annotated[UserService, Depends(get_user_service)]
WalletServiceDependable = Annotated[WalletService, Depends(get_wallet_service)]
