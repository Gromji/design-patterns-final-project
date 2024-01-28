from re import compile
from typing import Protocol

from wallet.core.entity.user import User
from wallet.core.error.errors import WrongEmailError


class IValidator(Protocol):
    @staticmethod
    def validate_user(user: User) -> None:
        pass


class DefaultValidator(IValidator):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    @staticmethod
    def validate_user(user: User) -> None:
        if not DefaultValidator.is_valid_email(user.email):
            raise WrongEmailError

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_pattern = compile(DefaultValidator.EMAIL_REGEX)
        match = email_pattern.match(email)

        return bool(match)
