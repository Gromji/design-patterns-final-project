import pytest

from wallet.core.entity.user import UserBuilder
from wallet.core.error.errors import AlreadyExistsError, DoesNotExistError
from wallet.core.facade import WalletService
from wallet.infra.repository.memory.user_repository import (
    UserRepository as InMemoryUserRepository,
)
from wallet.infra.repository.sqlite.connection_manager import ConnectionManager
from wallet.infra.repository.sqlite.user_repository import (
    UserRepository as PostgresUserRepository,
)


@pytest.fixture
def service_in_mem_dict() -> WalletService:
    return WalletService(InMemoryUserRepository())


@pytest.fixture
def service_in_mem_sqlite() -> WalletService:
    ConnectionManager.set_in_mem(True)
    return WalletService(PostgresUserRepository())


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_user_by_id(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    user = UserBuilder().builder().email("email@gmail.com").api_key("123").build()
    assert user.user_id == service.create_user(user).user_id
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_user_by_id(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.get_user_by_id("123")
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_already_exists_user_by_id(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    user = UserBuilder().builder().email("email@gmail.com").api_key("123").build()
    service.create_user(user)
    with pytest.raises(AlreadyExistsError):
        service.create_user(user)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_user_by_email(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    user = UserBuilder().builder().email("email@gmail.com").api_key("123").build()
    assert user.email == service.create_user(user).email
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_user_by_email(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.get_user_by_email("email@gmail.com")
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_already_exists_user_by_email(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    user = UserBuilder().builder().email("email@gmail.com").build()
    service.create_user(user)
    with pytest.raises(AlreadyExistsError):
        service.create_user(user)
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_api_key_by_id(service_name: str, request: pytest.FixtureRequest) -> None:
    service = request.getfixturevalue(service_name)
    user = UserBuilder().builder().email("email@gmail.com").api_key("123").build()
    assert user.api_key == service.create_user(user).api_key
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_api_key_by_id(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.get_api_key_by_id("123")
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_get_api_key_by_email(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    user = UserBuilder().builder().email("email@gmail.com").api_key("123").build()
    assert user.api_key == service.create_user(user).api_key
    service.tear_down()


@pytest.mark.parametrize(
    "service_name", ["service_in_mem_dict", "service_in_mem_sqlite"]
)
def test_not_found_api_key_by_email(
    service_name: str, request: pytest.FixtureRequest
) -> None:
    service = request.getfixturevalue(service_name)
    with pytest.raises(DoesNotExistError):
        service.get_api_key_by_email("email@gmail.com")
    service.tear_down()
