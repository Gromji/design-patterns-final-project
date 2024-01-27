from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Transaction:
    from_address: str
    to_address: str
    amount: int
    fee: int
    id: UUID = field(default_factory=uuid4)


class ITransactionBuilder(Protocol):
    def builder(self) -> ITransactionBuilder:
        pass

    def from_address(self, address: str) -> ITransactionBuilder:
        pass

    def to_address(self, address: str) -> ITransactionBuilder:
        pass

    def amount(self, amount: int) -> ITransactionBuilder:
        pass

    def fee(self, fee: int) -> ITransactionBuilder:
        pass

    def id(self, t_id: UUID) -> ITransactionBuilder:
        pass

    def build(self) -> Transaction:
        pass


class TransactionBuilder(ITransactionBuilder):
    transaction: Transaction

    def builder(self) -> ITransactionBuilder:
        self.transaction = Transaction(from_address="", to_address="", amount=0, fee=0)
        return self

    def from_address(self, address: str) -> ITransactionBuilder:
        self.transaction.from_address = address
        return self

    def to_address(self, address: str) -> ITransactionBuilder:
        self.transaction.to_address = address
        return self

    def amount(self, amount: int) -> ITransactionBuilder:
        self.transaction.amount = amount
        return self

    def fee(self, fee: int) -> ITransactionBuilder:
        self.transaction.fee = fee
        return self

    def id(self, t_id: UUID) -> ITransactionBuilder:
        self.transaction.id = t_id
        return self

    def build(self) -> Transaction:
        return self.transaction
