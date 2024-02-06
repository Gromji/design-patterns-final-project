from typing import Callable, Protocol

fee_percentage = 0.015


def default_fee_calculating_strategy(amount: int) -> int:
    return max(int(amount * fee_percentage), 1)


class IFeeCalculator(Protocol):
    @staticmethod
    def calculate_fee(
        amount: int, fee_calculating_strategy: Callable[[int], int]
    ) -> int:
        pass


class FeeCalculator(IFeeCalculator):
    @staticmethod
    def calculate_fee(
        amount: int,
        fee_calculating_strategy: Callable[
            [int], int
        ] = default_fee_calculating_strategy,
    ) -> int:
        return fee_calculating_strategy(amount)
