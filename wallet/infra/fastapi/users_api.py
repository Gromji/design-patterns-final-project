from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from wallet.core.entity.user import UserBuilder
from wallet.core.error.errors import WrongEmailError, AlreadyExistsError
from wallet.infra.fastapi.dependables import UserServiceDependable

users_api = APIRouter()


class APIResponse(BaseModel):
    api_key: str


class CreateUserRequest(BaseModel):
    email: str


@users_api.post("/", status_code=201, response_model=APIResponse)
def create_user(
    create_request: CreateUserRequest, service: UserServiceDependable
) -> Dict[str, str] | JSONResponse:
    user = UserBuilder().builder().email(create_request.email).build()
    try:
        return {"api_key": service.create_user(user).api_key}
    except Exception as err:
        return JSONResponse(
            status_code=409,
            content={"error": {"message": err.args}},
        )
