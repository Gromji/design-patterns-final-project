from typing import List
from uuid import UUID

from wallet.core.entity.transaction import Transaction
from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet
from wallet.infra.repository.repository_interface import (
    IUserRepository,
    IWalletRepository,
    ITransactionRepository
)


class UserService:
    user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: UUID) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)

    def create_user(self, user: User) -> User:
        return self.user_repository.create_user(user)

    def get_api_key_by_id(self, user_id: UUID) -> str:
        return self.user_repository.get_api_key_by_id(user_id)

    def get_api_key_by_email(self, email: str) -> str:
        return self.user_repository.get_api_key_by_email(email)

    def tear_down(self) -> None:
        self.user_repository.tear_down()


class TransactionService:
    # TODO: probably need wallet repository as well
    transaction_repository: ITransactionRepository

    def __init__(self, transaction_repository: ITransactionRepository) -> None:
        self.transaction_repository = transaction_repository

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction:
        return self.transaction_repository.get_transaction_by_id(transaction_id)

    def get_all_transactions(self) -> List[Transaction]:
        return self.transaction_repository.get_all_transactions()

    def create_transaction(self, transaction: Transaction) -> Transaction:
        # TODO: probably need to interact with wallet repository as well
        return self.transaction_repository.create_transaction(transaction)

    def filter_transactions(self, wallet: Wallet) -> List[Transaction]:
        return self.transaction_repository.filter_transactions(wallet)

    def tear_down(self) -> None:
        self.transaction_repository.tear_down()


class WalletService:
    wallet_repository: IWalletRepository

    def __init__(self, wallet_repository: IWalletRepository) -> None:
        self.wallet_repository = wallet_repository

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
