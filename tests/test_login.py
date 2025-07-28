"""Tests for the login."""

import pytest
from aioresponses import aioresponses
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
async def test_auth__should_raise_error_when_non_2xx_status_code(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test that non-2xx status codes raise MyLightSystemsError."""
    # Given
    responses.get(
        _AUTH_URL,
        status=status,
    )

    # When / Then
    with pytest.raises(MyLightSystemsError):
        await client.auth(email="fake", password="fake")


async def test_auth__should_raise_invalid_auth_error_when_bad_credentials(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that bad credentials raise MyLightSystemsInvalidAuthError."""
    # Given
    email = "fake_email@fake.com"
    password = "fake_password"

    responses.get(
        f"{_AUTH_URL}?email={email}&password={password}",
        status=200,
        body=load_fixture("login_failed.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsInvalidAuthError):
        await client.auth(email=email, password=password)


async def test_auth__should_return_token_when_valid_credentials(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that valid credentials return authentication token."""
    # Given
    email = "fake_email@fake.com"
    password = "fake_password"

    responses.get(
        f"{_AUTH_URL}?email={email}&password={password}",
        status=200,
        body=load_fixture("login_success.json"),
    )

    # When
    response = await client.auth(email=email, password=password)

    # Then
    assert response is not None
    assert "fake_auth_token" == response.token
