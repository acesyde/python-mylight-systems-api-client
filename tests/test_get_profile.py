"""Tests for get profile."""

from aioresponses import aioresponses
import pytest

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
async def test_get_profile_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        f"{_PROFILE_URL}?authToken=fake-token",
        status=status,
    )
    with pytest.raises(MyLightSystemsError):
        await client.get_profile(auth_token="fake-token")


async def test_get_profile_with_bad_token_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad token call."""
    responses.get(
        f"{_PROFILE_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_profile(auth_token="fake-token")


async def test_get_profile_success_return_profile(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test get profile call."""
    responses.get(
        f"{_PROFILE_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("profile.json"),
    )
    response = await client.get_profile(auth_token="fake-token")
    assert response is not None
    assert response.id is not None
    assert response.grid_type is not None
    assert response.id == "fake_user_id"
    assert response.grid_type == "1 phase"
