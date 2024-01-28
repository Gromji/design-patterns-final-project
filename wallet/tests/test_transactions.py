from uuid import uuid4

import pytest

from wallet.core.entity.transaction import TransactionBuilder
from wallet.core.entity.wallet import WalletBuilder
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.core.facade import TransactionService
from wallet.infra.repository.memory.transaction_repository import (
    TransactionRepository as InMemoryTransactionRepository,
)
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.transaction_repository import (
    TransactionRepository as SqliteTransactionRepository,
)


@pytest.fixture
def service_in_mem_dict() -> TransactionService:
    return TransactionService(InMemoryTransactionRepository())


@pytest.fixture
def service_in_mem_sqlite() -> TransactionService:
    ConnectionManager.set_foreign_keys(False)
    ConnectionManager.set_in_mem(True)
    return TransactionService(SqliteTransactionRepository())


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
        .amount(100)
        .build()
    )
    assert transaction.id == service.create_transaction(transaction).id
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
        .amount(100)
        .build()
    )
    service.create_transaction(transaction)
    retrieved_transaction = service.get_transaction_by_id(transaction.id)
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
        .amount(100)
        .build()
    )
    service.create_transaction(transaction)
    with pytest.raises(AlreadyExistsError):
        service.create_transaction(transaction)
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
        .amount(100)
        .build()
    )
    service.create_transaction(transaction_1)
    service.create_transaction(transaction_2)
    service.create_transaction(transaction_3)
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
        .amount(100)
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
    service.create_transaction(transaction_1)
    service.create_transaction(transaction_2)
    all_transactions = service.get_all_transactions()
    assert len(all_transactions) == 2
    service.tear_down()
