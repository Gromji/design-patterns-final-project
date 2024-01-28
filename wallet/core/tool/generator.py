import uuid
from typing import Protocol


class IApiKeyGen(Protocol):
    def generate(self) -> str:
        pass


class ApiKeyGen(IApiKeyGen):
    def generate(self) -> str:
        return str(uuid.uuid4())
