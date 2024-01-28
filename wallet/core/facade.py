from dataclasses import dataclass, field
from typing import List, Type
from uuid import UUID

from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet
from wallet.core.tool.generator import DefaultGenerator, IGenerator
from wallet.core.tool.validator import DefaultValidator, IValidator
from wallet.infra.repository.repository_interface import (
    IUserRepository,
    IWalletRepository,
)


@dataclass
class UserService:
    user_repository: IUserRepository
    generator: IGenerator = field(default_factory=DefaultGenerator)
    validator: Type[IValidator] = field(default=DefaultValidator)

    def get_user_by_id(self, user_id: UUID) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)

    def create_user(self, user: User) -> User:
        if user.api_key == "":
            user.api_key = self.generator.generate_api_key()
        self.validator.validate_user(user)
        return self.user_repository.create_user(user)

    def get_api_key_by_id(self, user_id: UUID) -> str:
        return self.user_repository.get_api_key_by_id(user_id)

    def get_api_key_by_email(self, email: str) -> str:
        return self.user_repository.get_api_key_by_email(email)

    def tear_down(self) -> None:
        self.user_repository.tear_down()


@dataclass
class WalletService:
    wallet_repository: IWalletRepository

    def create_wallet(self, wallet: Wallet) -> Wallet:
        return self.wallet_repository.create_wallet(wallet)

    def get_wallet(self, address: str) -> Wallet:
        return self.wallet_repository.get_wallet(address)

    def get_user_wallets(self, user: User) -> List[Wallet]:
        return self.wallet_repository.get_user_wallets(user)

    def update_amount(self, address: str, amount: int) -> Wallet:
        return self.wallet_repository.update_amount(address, amount)

    def tear_down(self) -> None:
        self.wallet_repository.tear_down()
