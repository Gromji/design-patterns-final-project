import sqlite3
from typing import List

DATABASE_NAME = "wallet.db"


class ConnectionManager:
    connections: List[sqlite3.Connection] = []
    in_mem: bool = False

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        if len(ConnectionManager.connections) == 0:
            ConnectionManager.connections.append(
                sqlite3.connect(DATABASE_NAME, check_same_thread=False)
                if not ConnectionManager.in_mem
                else sqlite3.connect(
                    "file::memory:?cache=shared", check_same_thread=False
                )
            )
        conn = ConnectionManager.connections[0]
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.close()
        return ConnectionManager.connections[0]

    @staticmethod
    def set_in_mem(in_mem: bool) -> None:
        ConnectionManager.in_mem = in_mem

    @staticmethod
    def close_all() -> None:
        for connection in ConnectionManager.connections:
            connection.close()
