from re import compile
from typing import Protocol

from wallet.core.entity.user import User
from wallet.core.entity.wallet import Wallet
from wallet.core.error.errors import WrongEmailError, WrongOwnerError


class IValidator(Protocol):
    @staticmethod
    def validate_user(user: User) -> None:
        pass

    @staticmethod
    def validate_wallet(wallet: Wallet) -> None:
        pass

    @staticmethod
    def validate_wallet_owner(wallet: Wallet, user: User) -> None:
        pass


class DefaultValidator(IValidator):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    @staticmethod
    def validate_user(user: User) -> None:
        if not DefaultValidator.is_valid_email(user.email):
            raise WrongEmailError(f"Wrong email: {user.email}")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_pattern = compile(DefaultValidator.EMAIL_REGEX)
        match = email_pattern.match(email)

        return bool(match)

    @staticmethod
    def validate_wallet_owner(wallet: Wallet, user: User) -> None:
        if wallet.user_id != user.user_id:
            raise WrongOwnerError(f"Wrong owner! api_key: {user.api_key}")
