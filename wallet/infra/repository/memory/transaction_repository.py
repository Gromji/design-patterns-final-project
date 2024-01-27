from typing import List, Dict
from uuid import UUID

from wallet.core.entity.transaction import Transaction
from wallet.core.error.errors import DoesNotExistError, AlreadyExistsError
from wallet.infra.repository.repository_interface import ITransactionRepository


class TransactionRepository(ITransactionRepository):
    def __init__(self) -> None:
        self.transactions: Dict[UUID, Transaction] = {}

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction:
        try:
            return self.transactions[transaction_id]
        except KeyError:
            raise DoesNotExistError(f"Transaction with id {str(transaction_id)} not found")

    def get_all_transactions(self) -> List[Transaction]:
        return [v for v in self.transactions.values()]

    def create_transaction(self, transaction: Transaction) -> Transaction:
        if transaction.id in self.transactions:
            raise AlreadyExistsError(f"Transaction with id {str(transaction.id)} already exists")

        self.transactions[transaction.id] = transaction
        return transaction

    def filter_transactions(self, wallet: "Wallet") -> List[Transaction]:
        pass

    def tear_down(self) -> None:
        self.transactions = {}