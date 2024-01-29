from typing import Protocol

import requests

from wallet.core.error.errors import ConversionError

BTC_TO_SATOSHI = 100_000_000
DEFAULT_WALLET_BALANCE = BTC_TO_SATOSHI


class IConverter(Protocol):
    def btc_to_usd(self, value: float) -> float:
        pass

    def satoshi_to_usd(self, value: int) -> float:
        pass

    @staticmethod
    def btc_to_satoshi(value: float) -> int:
        pass

    @staticmethod
    def satoshi_to_btc(value: int) -> float:
        pass


class Converter(IConverter):
    def __init__(self, url: str = "https://blockchain.info"):
        self.url = url

    def btc_to_usd(self, value: float) -> float:
        response: requests.Response = requests.get(f"{self.url}/ticker")
        if response.status_code == 200:
            return value * float(response.json()["USD"]["last"])

        raise ConversionError("Error when trying to convert BTC to USD")

    @staticmethod
    def btc_to_satoshi(value: float) -> int:
        return int(value * BTC_TO_SATOSHI)

    @staticmethod
    def satoshi_to_btc(value: int) -> float:
        return value / BTC_TO_SATOSHI
