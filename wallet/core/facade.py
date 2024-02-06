from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from wallet.core.entity.transaction import Transaction
from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet
from wallet.core.error.errors import NotEnoughBalanceError
from wallet.core.tool.generator import DefaultGenerator, IGenerator
from wallet.core.tool.validator import DefaultValidator, IValidator
from wallet.infra.repository.repository_interface import (
    ITransactionRepository,
    IUserRepository,
    IWalletRepository,
)


@dataclass
class UserService:
    user_repository: IUserRepository
    generator: IGenerator = field(default_factory=DefaultGenerator)
    validator: IValidator = field(default_factory=DefaultValidator)

    def get_user_by_id(self, user_id: UUID) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)

    def get_user_by_api_key(self, api_key: str) -> User:
        return self.user_repository.get_user_by_api_key(api_key)

    def create_user(self, user: User) -> User:
        user.api_key = user.api_key or self.generator.generate_api_key()
        self.validator.validate_user(user)
        return self.user_repository.create_user(user)

    def get_api_key_by_id(self, user_id: UUID) -> str:
        return self.user_repository.get_api_key_by_id(user_id)

    def get_api_key_by_email(self, email: str) -> str:
        return self.user_repository.get_api_key_by_email(email)

    def tear_down(self) -> None:
        self.user_repository.tear_down()


@dataclass
class TransactionService:
    transaction_repository: ITransactionRepository
    wallet_repository: IWalletRepository
    validator: IValidator = field(default_factory=DefaultValidator)
    _fee: float = 0.015

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction:
        return self.transaction_repository.get_transaction_by_id(transaction_id)

    def get_all_transactions(self) -> List[Transaction]:
        return self.transaction_repository.get_all_transactions()

    def create_transaction(
        self, transaction: Transaction, sender: User, validate_sender: bool = True
    ) -> Transaction:
        from_wallet = self.wallet_repository.get_wallet(transaction.from_address)
        if validate_sender:
            self.validator.validate_wallet_owner(from_wallet, sender)
        to_wallet = self.wallet_repository.get_wallet(transaction.to_address)

        fee = max(int(transaction.amount * self._fee), 1)

        if from_wallet.amount < transaction.amount + fee:
            raise NotEnoughBalanceError("Not enough balance in the wallet.")

        transaction.fee = fee
        tx = self.transaction_repository.create_transaction(transaction)

        from_wallet_new_amount, to_wallet_new_amount = (
            from_wallet.amount - transaction.amount,
            to_wallet.amount + transaction.amount,
        )
        self.wallet_repository.update_amount(
            from_wallet.address, from_wallet_new_amount
        )
        self.wallet_repository.update_amount(to_wallet.address, to_wallet_new_amount)

        return tx

    def filter_transactions(self, wallet: Wallet) -> List[Transaction]:
        return self.transaction_repository.filter_transactions(wallet)

    def get_transaction_count(self) -> int:
        return self.transaction_repository.get_transaction_count()

    def get_profit(self) -> int:
        return self.transaction_repository.get_profit()

    def tear_down(self) -> None:
        self.transaction_repository.tear_down()
        self.wallet_repository.tear_down()


@dataclass
class WalletService:
    wallet_repository: IWalletRepository
    generator: IGenerator = field(default_factory=DefaultGenerator)
    validator: IValidator = field(default_factory=DefaultValidator)

    def create_wallet(self, wallet: Wallet) -> Wallet:
        wallet.address = wallet.address or self.generator.generate_wallet_address()
        return self.wallet_repository.create_wallet(wallet)

    def get_wallet(
        self, address: str, user: User, validate_owner: bool = True
    ) -> Wallet:
        wallet = self.wallet_repository.get_wallet(address)
        if validate_owner:
            self.validator.validate_wallet_owner(wallet, user)
        return wallet

    def get_user_wallets(self, user: User) -> List[Wallet]:
        return self.wallet_repository.get_user_wallets(user)

    def update_amount(self, address: str, amount: int) -> Wallet:
        return self.wallet_repository.update_amount(address, amount)

    def tear_down(self) -> None:
        self.wallet_repository.tear_down()
