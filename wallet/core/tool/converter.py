from typing import Protocol

import requests

from wallet.core.error.errors import ConversionError


class IConverter(Protocol):
    def to_usd(self, value: float) -> float:
        pass


class Converter(IConverter):
    def __init__(self, url: str = "https://blockchain.info"):
        self.url = url

    def to_usd(self, value: float) -> float:
        response: requests.Response = requests.get(f"{self.url}/ticker")
        if response.status_code == 200:
            return value * float(response.json()["USD"]["last"])

        raise ConversionError("Error when trying to convert BTC to USD")
