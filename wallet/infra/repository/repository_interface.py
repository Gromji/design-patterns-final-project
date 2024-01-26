from typing import Protocol, List
from uuid import UUID

from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet


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


class IWalletRepository(Protocol):
    def get_wallet(self, address: str) -> Wallet:
        pass

    def create_wallet(self, wallet: Wallet) -> Wallet:
        pass

    def get_user_wallets(self, user: User) -> List[Wallet]:
        pass

    def update_amount(self, address: str, amount: int) -> Wallet:
        pass

    def tear_down(self) -> None:
        pass
