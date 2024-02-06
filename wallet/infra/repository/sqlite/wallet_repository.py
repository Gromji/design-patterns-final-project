from contextlib import closing
from typing import List
from uuid import UUID

from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.infra.repository.repository_interface import IWalletRepository
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.user_repository import USER_TABLE_NAME

WALLET_TABLE_NAME = "wallets"


class WalletRepository(IWalletRepository):
    def __init__(self) -> None:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {WALLET_TABLE_NAME} (
                    Address TEXT PRIMARY KEY,
                    Amount INTEGER,
                    User_ID TEXT,
                    FOREIGN KEY (User_ID) REFERENCES {USER_TABLE_NAME}(ID)
                );"""
            )

    def get_wallet(self, address: str) -> Wallet:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"SELECT * FROM {WALLET_TABLE_NAME} WHERE address = ?", (address,)
            )
            wallet = cursor.fetchone()
            if wallet is None:
                raise DoesNotExistError(f"Wallet with address {address} not found")
            return Wallet(address=wallet[0], amount=wallet[1], user_id=UUID(wallet[2]))

    def create_wallet(self, wallet: Wallet) -> Wallet:
        conn = ConnectionManager.get_connection()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    f"INSERT INTO {WALLET_TABLE_NAME} VALUES (?, ?, ?)",
                    (str(wallet.address), wallet.amount, str(wallet.user_id)),
                )
        except Exception as e:
            raise AlreadyExistsError(
                f"Wallet with address {wallet.address} already exists"
            ) from e
        return wallet

    def get_user_wallets(self, user: User) -> List[Wallet]:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"SELECT * FROM {WALLET_TABLE_NAME}" f" WHERE user_id = ?",
                (str(user.user_id),),
            )
            wallets = cursor.fetchall()

            return [
                Wallet(address=wallet[0], amount=wallet[1], user_id=UUID(wallet[2]))
                for wallet in wallets
            ]

    def update_amount(self, address: str, amount: int) -> Wallet:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"UPDATE {WALLET_TABLE_NAME} " f"SET amount = ? WHERE address = ?",
                (
                    amount,
                    address,
                ),
            )
            if cursor.rowcount == 0:
                raise DoesNotExistError(
                    f"Wallet with address" f" {address} does not exist"
                )

        return self.get_wallet(address)

    def tear_down(self) -> None:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"DROP TABLE {WALLET_TABLE_NAME}")
