from typing import Protocol

import requests

from wallet.core.error.errors import ConversionError

BTC_TO_SATOSHI = 100_000_000
DEFAULT_WALLET_BALANCE = BTC_TO_SATOSHI


class IConverter(Protocol):
    @staticmethod
    def btc_to_usd(value: float) -> float:
        pass

    @staticmethod
    def satoshi_to_usd(value: int) -> float:
        pass

    @staticmethod
    def btc_to_satoshi(value: float) -> int:
        pass

    @staticmethod
    def satoshi_to_btc(value: int) -> float:
        pass


class Converter(IConverter):
    @staticmethod
    def btc_to_usd(value: float, url: str = "https://blockchain.info") -> float:
        response: requests.Response = requests.get(f"{url}/ticker")
        if response.status_code == 200:
            return value * float(response.json()["USD"]["last"])

        raise ConversionError("Error when trying to convert BTC to USD")

    @staticmethod
    def satoshi_to_usd(value: int) -> float:
        return Converter.btc_to_usd(Converter.satoshi_to_btc(value))

    @staticmethod
    def btc_to_satoshi(value: float) -> int:
        return int(value * BTC_TO_SATOSHI)

    @staticmethod
    def satoshi_to_btc(value: int) -> float:
        return value / BTC_TO_SATOSHI
