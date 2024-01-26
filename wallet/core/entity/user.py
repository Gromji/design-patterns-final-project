from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class User:
    email: str
    api_key: str
    user_id: UUID = field(default_factory=uuid4)


class IUserBuilder(Protocol):
    def builder(self) -> "IUserBuilder":
        pass

    def email(self, email: str) -> "IUserBuilder":
        pass

    def api_key(self, api_key: str) -> "IUserBuilder":
        pass

    def user_id(self, user_id: UUID) -> "IUserBuilder":
        pass

    def build(self) -> User:
        pass


class UserBuilder(IUserBuilder):
    user: User

    def builder(self) -> IUserBuilder:
        self.user = User(user_id=uuid4(), email="", api_key="")
        return self

    def email(self, email: str) -> IUserBuilder:
        self.user.email = email
        return self

    def api_key(self, api_key: str) -> IUserBuilder:
        self.user.api_key = api_key
        return self

    def user_id(self, user_id: UUID) -> IUserBuilder:
        self.user.user_id = user_id
        return self

    def build(self) -> User:
        return self.user
