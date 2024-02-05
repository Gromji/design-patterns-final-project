from typing import Dict, List
from uuid import UUID

from wallet.core.entity.transaction import Transaction
from wallet.core.entity.wallet import Wallet
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.infra.repository.repository_interface import ITransactionRepository


class TransactionRepository(ITransactionRepository):
    def __init__(self) -> None:
        self.transactions: Dict[UUID, Transaction] = {}

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction:
        try:
            return self.transactions[transaction_id]
        except KeyError:
            raise DoesNotExistError(
                f"Transaction with id {str(transaction_id)} not found"
            )

    def get_all_transactions(self) -> List[Transaction]:
        return [v for v in self.transactions.values()]

    def create_transaction(self, transaction: Transaction) -> Transaction:
        if transaction.transaction_id in self.transactions:
            raise AlreadyExistsError(
                f"Transaction with id {str(transaction.transaction_id)} already exists"
            )

        self.transactions[transaction.transaction_id] = transaction
        return transaction

    def filter_transactions(self, wallet: Wallet) -> List[Transaction]:
        return [
            v
            for v in self.transactions.values()
            if wallet.address in (v.from_address, v.to_address)
        ]

    def get_transaction_count(self) -> int:
        return len(self.transactions)

    def get_profit(self) -> int:
        return sum(v.fee for v in self.transactions.values())

    def tear_down(self) -> None:
        self.transactions = {}
