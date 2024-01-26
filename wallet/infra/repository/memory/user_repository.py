from typing import Dict
from uuid import UUID

from wallet.core.entity.user import User
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.infra.repository.repository_interface import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self) -> None:
        self.users: Dict[UUID, User] = {}

    def get_user_by_id(self, user_id: UUID) -> User:
        try:
            return self.users[user_id]
        except KeyError:
            raise DoesNotExistError(f"User with id {user_id} not found")

    def get_user_by_email(self, email: str) -> User:
        for user in self.users.values():
            if user.email == email:
                return user
        raise DoesNotExistError(f"User with email {email} not found")

    def create_user(self, user: User) -> User:
        if user.user_id in self.users:
            raise AlreadyExistsError(f"User with id {user.user_id} already exists")

        if [u for u in self.users.values() if u.email == user.email]:
            raise AlreadyExistsError(f"User with email {user.email} already exists")

        self.users[user.user_id] = user
        return user

    def get_api_key_by_id(self, user_id: UUID) -> str:
        return self.get_user_by_id(user_id).api_key

    def get_api_key_by_email(self, email: str) -> str:
        return self.get_user_by_email(email).api_key

    def tear_down(self) -> None:
        self.users = {}
