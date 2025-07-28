"""Tests for get profile."""

import pytest
from aioresponses import aioresponses
from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)

from tests import load_fixture
from tests.const import MOCK_URL

_PROFILE_URL = f"{MOCK_URL}/api/profile"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_get_profile__should_raise_error_when_non_2xx_status_code(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test that non-2xx status codes raise MyLightSystemsError."""
    # Given
    responses.get(
        f"{_PROFILE_URL}?authToken=fake-token",
        status=status,
    )

    # When / Then
    with pytest.raises(MyLightSystemsError):
        await client.get_profile(auth_token="fake-token")


async def test_get_profile__should_raise_unauthorized_error_when_bad_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that bad token raises MyLightSystemsUnauthorizedError."""
    # Given
    responses.get(
        f"{_PROFILE_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_profile(auth_token="fake-token")


async def test_get_profile__should_return_profile_when_valid_request(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that valid request returns profile data."""
    # Given
    responses.get(
        f"{_PROFILE_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("profile.json"),
    )

    # When
    response = await client.get_profile(auth_token="fake-token")

    # Then
    assert response is not None
    assert response.id is not None
    assert response.grid_type is not None
    assert "fake_user_id" == response.id
    assert "1 phase" == response.grid_type
    assert "myhome" == response.tenant
    assert "Lourdes" == response.city
    assert "FR" == response.country
    assert "11111" == response.postal_code
    assert "10 rue de la gare" == response.address
