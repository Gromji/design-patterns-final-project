from typing import List
from uuid import UUID

from wallet.core.entity.transaction import Transaction
from wallet.infra.repository.repository_interface import ITransactionRepository


class TransactionRepository(ITransactionRepository):
    def __init__(self) -> None:
        pass

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction:
        pass

    def get_all_transactions(self) -> List[Transaction]:
        pass

    def create_transaction(self, transaction: Transaction) -> Transaction:
        pass

    def filter_transactions(self, wallet: "Wallet") -> List[Transaction]:
        pass

    def tear_down(self) -> None:
        pass
