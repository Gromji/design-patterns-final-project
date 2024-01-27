from typing import List, Dict

from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet
from wallet.core.error.errors import DoesNotExistError, AlreadyExistsError
from wallet.infra.repository.repository_interface import IWalletRepository


class WalletRepository(IWalletRepository):
    wallets: Dict[str, Wallet]

    def __init__(self) -> None:
        self.wallets = {}

    def get_wallet(self, address: str) -> Wallet:
        try:
            return self.wallets[address]
        except KeyError:
            raise DoesNotExistError(f"Wallet with address {address} not found")

    def create_wallet(self, wallet: Wallet) -> Wallet:
        if wallet.address in self.wallets:
            raise AlreadyExistsError(f"Wallet with address {wallet.address} already exists")

        self.wallets[wallet.address] = wallet
        return wallet

    def get_user_wallets(self, user: User) -> List[Wallet]:
        return [self.wallets[a] for a in self.wallets
                if self.wallets[a].user_id == user.user_id]

    def update_amount(self, address: str, amount: int) -> Wallet:
        try:
            self.wallets[address].amount = amount
            return self.get_wallet(address)
        except KeyError:
            raise DoesNotExistError(f"Wallet with address {address} does not exist")

    def tear_down(self) -> None:
        self.wallets = {}
