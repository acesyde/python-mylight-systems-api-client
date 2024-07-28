"""Tests for the login."""

import aioresponses
import pytest

from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsInvalidAuthError,
)
from tests import load_fixture
from tests.const import MOCK_URL

_AUTH_URL = f"{MOCK_URL}/api/auth"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_login_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        _AUTH_URL,
        status=status,
    )
    with pytest.raises(MyLightSystemsError):
        await client.login(email="fake", password="fake")


async def test_login_with_bad_credentials_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad credentials call."""
    email = "fake_email@fake.com"
    password = "fake_password"

    responses.get(
        f"{_AUTH_URL}?email={email}&password={password}",
        status=200,
        body=load_fixture("login_failed.json"),
    )

    with pytest.raises(MyLightSystemsInvalidAuthError):
        await client.login(email=email, password=password)


async def test_login_success_return_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test login call."""
    email = "fake_email@fake.com"
    password = "fake_password"

    responses.get(
        f"{_AUTH_URL}?email={email}&password={password}",
        status=200,
        body=load_fixture("login_success.json"),
    )
    response = await client.login(email=email, password=password)
    assert response is not None
    assert response.token == "fake_auth_token"
