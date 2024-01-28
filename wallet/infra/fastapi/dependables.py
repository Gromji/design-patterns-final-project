from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from wallet.core.facade import UserService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service  # type: ignore


UserServiceDependable = Annotated[UserService, Depends(get_user_service)]
