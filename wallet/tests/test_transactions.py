from uuid import uuid4

import pytest

from wallet.core.entity.transaction import TransactionBuilder
from wallet.core.entity.wallet import Wallet, WalletBuilder
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.core.facade import TransactionService
from wallet.infra.repository.memory.transaction_repository import (
    TransactionRepository as InMemoryTransactionRepository,
)
from wallet.infra.repository.memory.wallet_repository import (
    WalletRepository as InMemoryWalletRepository,
)
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.transaction_repository import (
    TransactionRepository as SQLiteTransactionRepository,
)
from wallet.infra.repository.sqlite.wallet_repository import (
    WalletRepository as SQLiteWalletRepository,
)


@pytest.fixture
def service_in_mem_dict() -> TransactionService:
    ts = TransactionService(
        InMemoryTransactionRepository(),
        InMemoryWalletRepository(),
    )
    ts.wallet_repository.create_wallet(Wallet("address_1", 100, uuid4()))
    ts.wallet_repository.create_wallet(Wallet("address_2", 200, uuid4()))
    ts.wallet_repository.create_wallet(Wallet("address_3", 300, uuid4()))
    return ts


@pytest.fixture
def service_in_mem_sqlite() -> TransactionService:
    ConnectionManager.set_foreign_keys(False)
    ConnectionManager.set_in_mem(True)
    ts = TransactionService(SQLiteTransactionRepository(), SQLiteWalletRepository())
    ts.wallet_repository.create_wallet(Wallet("address_1", 100, uuid4()))
    ts.wallet_repository.create_wallet(Wallet("address_2", 200, uuid4()))
    ts.wallet_repository.create_wallet(Wallet("address_3", 300, uuid4()))
    return ts


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_create_transaction(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    transaction = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    assert (
        transaction.transaction_id
        == service.create_transaction(transaction, None, False).transaction_id
    )
    assert service.wallet_repository.get_wallet("address_1").amount == 50
    assert service.wallet_repository.get_wallet("address_2").amount == 250
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_transaction(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    transaction = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    service.create_transaction(transaction, None, False)
    retrieved_transaction = service.get_transaction_by_id(transaction.transaction_id)
    assert retrieved_transaction.amount == transaction.amount
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_transaction(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.get_transaction_by_id(uuid4())
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_already_exists_transaction(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    transaction = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    service.create_transaction(transaction, None, False)
    with pytest.raises(AlreadyExistsError):
        service.create_transaction(transaction, None, False)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_filter_transactions(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    transaction_3 = (
        TransactionBuilder()
        .builder()
        .from_address("address_3")
        .to_address("address_1")
        .amount(200)
        .build()
    )
    transaction_2 = (
        TransactionBuilder()
        .builder()
        .from_address("address_2")
        .to_address("address_3")
        .amount(200)
        .build()
    )
    transaction_1 = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    service.create_transaction(transaction_1, None, False)
    service.create_transaction(transaction_2, None, False)
    service.create_transaction(transaction_3, None, False)
    wallet = WalletBuilder().builder().address("address_2").build()
    filtered_transactions = service.filter_transactions(wallet)
    assert len(filtered_transactions) == 2
    assert all(
        "address_2" in (transaction.from_address, transaction.to_address)
        for transaction in filtered_transactions
    )
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_all_transactions(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    transaction_1 = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    transaction_2 = (
        TransactionBuilder()
        .builder()
        .from_address("address_2")
        .to_address("address_3")
        .amount(200)
        .build()
    )
    service.create_transaction(transaction_1, None, False)
    service.create_transaction(transaction_2, None, False)
    all_transactions = service.get_all_transactions()
    assert len(all_transactions) == 2
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_profit(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    transaction_1 = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    transaction_2 = (
        TransactionBuilder()
        .builder()
        .from_address("address_2")
        .to_address("address_3")
        .amount(200)
        .build()
    )
    service.create_transaction(transaction_1, None, False)
    service.create_transaction(transaction_2, None, False)
    assert service.get_profit() == int((50 + 200) * 0.015)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_transaction_count(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    transaction_1 = (
        TransactionBuilder()
        .builder()
        .from_address("address_1")
        .to_address("address_2")
        .amount(50)
        .build()
    )
    transaction_2 = (
        TransactionBuilder()
        .builder()
        .from_address("address_2")
        .to_address("address_3")
        .amount(200)
        .build()
    )
    service.create_transaction(transaction_1, None, False)
    service.create_transaction(transaction_2, None, False)
    assert service.get_transaction_count() == 2
    service.tear_down()
