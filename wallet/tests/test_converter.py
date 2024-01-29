import pytest

from wallet.core.tool.converter import Converter, IConverter


@pytest.fixture
def converter() -> IConverter:
    return Converter()


def test_converter_to_usd(converter: IConverter) -> None:
    assert converter.to_usd(1) > 0
