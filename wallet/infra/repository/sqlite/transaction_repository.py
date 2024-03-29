from contextlib import closing
from typing import List
from uuid import UUID

from wallet.core.entity.transaction import Transaction, TransactionBuilder
from wallet.core.entity.wallet import Wallet
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.infra.repository.repository_interface import ITransactionRepository
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.wallet_repository import WALLET_TABLE_NAME

TRANSACTION_TABLE_NAME = "transactions"


class TransactionRepository(ITransactionRepository):
    def __init__(self) -> None:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS Transactions (
                    id TEXT PRIMARY KEY,
                    From_Address TEXT,
                    To_Address TEXT,
                    Amount INTEGER,
                    Fee INTEGER,
                    FOREIGN KEY (From_Address)
                    REFERENCES {WALLET_TABLE_NAME}(Address),
                    FOREIGN KEY (To_Address)
                    REFERENCES {WALLET_TABLE_NAME}(Address)
                );"""
            )

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"SELECT * FROM {TRANSACTION_TABLE_NAME} WHERE id = ?",
                (str(transaction_id),),
            )
            transaction = cursor.fetchone()
            if transaction is None:
                raise DoesNotExistError(
                    f"Transaction with id {str(transaction_id)} not found"
                )
            return (
                TransactionBuilder()
                .builder()
                .transaction_id(transaction[0])
                .from_address(transaction[1])
                .to_address(transaction[1])
                .amount(int(transaction[3]))
                .fee(int(transaction[4]))
                .build()
            )

    def get_all_transactions(self) -> List[Transaction]:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TRANSACTION_TABLE_NAME}")
            transactions = cursor.fetchall()
            return [
                TransactionBuilder()
                .builder()
                .transaction_id(t[0])
                .from_address(t[1])
                .to_address(t[2])
                .amount(int(t[3]))
                .fee(int(t[4]))
                .build()
                for t in transactions
            ]

    def create_transaction(self, transaction: Transaction) -> Transaction:
        conn = ConnectionManager.get_connection()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    f"INSERT INTO {TRANSACTION_TABLE_NAME} VALUES (?, ?, ?, ?, ?)",
                    (
                        str(transaction.transaction_id),
                        transaction.from_address,
                        transaction.to_address,
                        transaction.amount,
                        transaction.fee,
                    ),
                )
        except Exception as e:
            raise AlreadyExistsError(
                f"Transaction with id {transaction.transaction_id} already exists"
            ) from e
        return transaction

    def filter_transactions(self, wallet: Wallet) -> List[Transaction]:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TRANSACTION_TABLE_NAME}")
            transactions = cursor.fetchall()
            return [
                TransactionBuilder()
                .builder()
                .transaction_id(t[0])
                .from_address(t[1])
                .to_address(t[2])
                .amount(int(t[3]))
                .fee(int(t[4]))
                .build()
                for t in transactions
                if wallet.address in (t[1], t[2])
            ]

    def get_transaction_count(self) -> int:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {TRANSACTION_TABLE_NAME}")
            return int(cursor.fetchone()[0])

    def get_profit(self) -> int:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT SUM(Fee) FROM {TRANSACTION_TABLE_NAME}")
            fetched = cursor.fetchone()
            if fetched[0] is None:
                return 0
            return int(fetched[0])

    def tear_down(self) -> None:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"DROP TABLE {TRANSACTION_TABLE_NAME}")
