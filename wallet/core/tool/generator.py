import uuid
from typing import Protocol


class IGenerator(Protocol):
    def generate_api_key(self) -> str:
        pass

    def generate_wallet_address(self) -> str:
        pass


class DefaultGenerator(IGenerator):
    def generate_api_key(self) -> str:
        return str(uuid.uuid4())

    def generate_wallet_address(self) -> str:
        return str(uuid.uuid4())
