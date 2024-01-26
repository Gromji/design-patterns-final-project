from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Wallet:
    address: str
    amount: float
    user_id: UUID


class IWalletBuilder(Protocol):
    def builder(self) -> IWalletBuilder:
        pass

    def address(self, address: str) -> IWalletBuilder:
        pass

    def amount(self, amount: float) -> IWalletBuilder:
        pass

    def user_id(self, user_id: UUID) -> IWalletBuilder:
        pass

    def build(self) -> Wallet:
        pass


class IWallet(IWalletBuilder):
    wallet: Wallet

    def builder(self) -> IWalletBuilder:
        self.wallet = Wallet(address="", amount=0.0, user_id=uuid4())
        return self

    def address(self, address: str) -> IWalletBuilder:
        self.wallet.address = address
        return self

    def amount(self, amount: float) -> IWalletBuilder:
        self.wallet.amount = amount
        return self

    def user_id(self, user_id: UUID) -> IWalletBuilder:
        self.wallet.user_id = user_id
        return self

    def build(self) -> Wallet:
        return self.wallet
