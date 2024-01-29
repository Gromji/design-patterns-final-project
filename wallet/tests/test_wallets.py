import pytest

from wallet.core.entity.user import UserBuilder
from wallet.core.entity.wallet import WalletBuilder
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.core.facade import WalletService
from wallet.infra.repository.memory.wallet_repository import (
    WalletRepository as InMemoryWalletRepository,
)
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.wallet_repository import (
    WalletRepository as SqliteWalletRepository,
)


@pytest.fixture
def service_in_mem_dict() -> WalletService:
    return WalletService(InMemoryWalletRepository())


@pytest.fixture
def service_in_mem_sqlite() -> WalletService:
    ConnectionManager.set_in_mem(True)
    ConnectionManager.set_foreign_keys(False)
    return WalletService(SqliteWalletRepository())


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_create_wallet(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    wallet = WalletBuilder().builder().address("address_1").amount(100).build()
    assert wallet.address == service.create_wallet(wallet).address
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_wallet(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    wallet = WalletBuilder().builder().address("address_1").amount(100).build()
    service.create_wallet(wallet)
    wallet1 = service.get_wallet("address_1", UserBuilder().builder().build(), False)
    assert wallet.amount == wallet1.amount and wallet.user_id == wallet1.user_id
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_wallet(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.get_wallet("address_1", UserBuilder().builder().build(), False)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_wallet_on_update(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.update_amount("address_1", 100)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_already_exists_wallet(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    wallet = WalletBuilder().builder().address("address_1").amount(100).build()
    service.create_wallet(wallet)
    with pytest.raises(AlreadyExistsError):
        service.create_wallet(wallet)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_user_wallets(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    user_1 = UserBuilder().builder().email("user1@example.com").api_key("123").build()
    user_2 = UserBuilder().builder().email("user2@example.com").api_key("456").build()
    wallet_1 = (
        WalletBuilder()
        .builder()
        .address("address_1")
        .amount(100)
        .user_id(user_1.user_id)
        .build()
    )
    wallet_2 = (
        WalletBuilder()
        .builder()
        .address("address_2")
        .amount(200)
        .user_id(user_1.user_id)
        .build()
    )
    wallet_3 = (
        WalletBuilder()
        .builder()
        .address("address_3")
        .amount(300)
        .user_id(user_2.user_id)
        .build()
    )
    service.create_wallet(wallet_1)
    service.create_wallet(wallet_2)
    service.create_wallet(wallet_3)
    wallets = service.get_user_wallets(user_1)
    assert len(wallets) == 2
    assert all(wallet.user_id == user_1.user_id for wallet in wallets)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_update_amount(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    wallet = WalletBuilder().builder().address("address_1").amount(100).build()
    service.create_wallet(wallet)
    new_amount = 200
    updated_wallet = service.update_amount("address_1", new_amount)
    assert updated_wallet.amount == new_amount
    service.tear_down()
