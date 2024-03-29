from contextlib import closing
from uuid import UUID

from wallet.core.entity.user import User
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.infra.repository.repository_interface import IUserRepository
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager

USER_TABLE_NAME = "users"


class UserRepository(IUserRepository):
    def __init__(self) -> None:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
                    id TEXT PRIMARY KEY, email TEXT UNIQUE, api_key TEXT UNIQUE
                    )"""
            )

    def get_user_by_id(self, user_id: UUID) -> User:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {USER_TABLE_NAME} WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if user is None:
                raise DoesNotExistError(f"User with id {user_id} not found")
            return User(user_id=UUID(user[0]), email=user[1], api_key=user[2])

    def get_user_by_email(self, email: str) -> User:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {USER_TABLE_NAME} WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user is None:
                raise DoesNotExistError(f"User with email {email} not found")
            return User(user_id=UUID(user[0]), email=user[1], api_key=user[2])

    def get_user_by_api_key(self, api_key: str) -> User:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f"SELECT * FROM {USER_TABLE_NAME} WHERE api_key = ?", (api_key,)
            )
            user = cursor.fetchone()
            if user is None:
                raise DoesNotExistError(f"User with api_key {api_key} not found")
            return User(user_id=UUID(user[0]), email=user[1], api_key=user[2])

    def create_user(self, user: User) -> User:
        conn = ConnectionManager.get_connection()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    f"INSERT INTO {USER_TABLE_NAME} VALUES (?, ?, ?)",
                    (str(user.user_id), user.email, user.api_key),
                )
        except Exception as e:
            raise AlreadyExistsError(
                f"User with id {user.user_id} already exists"
            ) from e
        return user

    def get_api_key_by_id(self, user_id: UUID) -> str:
        return self.get_user_by_id(user_id).api_key

    def get_api_key_by_email(self, email: str) -> str:
        return self.get_user_by_email(email).api_key

    def tear_down(self) -> None:
        conn = ConnectionManager.get_connection()
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"DROP TABLE {USER_TABLE_NAME}")
