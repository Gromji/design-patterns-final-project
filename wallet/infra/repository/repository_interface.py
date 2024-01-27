from typing import Protocol
from uuid import UUID

from wallet.core.entity.user import User


class IUserRepository(Protocol):
    def get_user_by_id(self, user_id: UUID) -> User:
        pass

    def get_user_by_email(self, email: str) -> User:
        pass

    def create_user(self, user: User) -> User:
        pass

    def get_api_key_by_id(self, user_id: UUID) -> str:
        pass

    def get_api_key_by_email(self, email: str) -> str:
        pass

    def tear_down(self) -> None:
        pass