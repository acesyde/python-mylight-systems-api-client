"""Tests for get devices."""

from aioresponses import aioresponses
import pytest

from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)
from tests import load_fixture
from tests.const import MOCK_URL

_DEVICE_URL = f"{MOCK_URL}/api/devices"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_get_devices_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        f"{_DEVICE_URL}?authToken=fake-token",
        status=status,
    )
    with pytest.raises(MyLightSystemsError):
        await client.get_devices(auth_token="fake-token")


async def test_get_devices_with_bad_token_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad token call."""
    responses.get(
        f"{_DEVICE_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_devices(auth_token="fake-token")


async def test_get_devices_success_return_devices(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test get profile call."""
    responses.get(
        f"{_DEVICE_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("devices.json"),
    )
    response = await client.get_devices(auth_token="fake-token")
    assert response is not None
    assert len(response) == 8

    first_device = response[0]
    assert first_device.id == "4D9F3281C75E"
    assert first_device.name == "Relais"
    assert first_device.type == "sw"

    first_device = response[7]
    assert first_device.id == "E9BC5FA11C75E"
    assert first_device.name == "Battery 1"
    assert first_device.type == "bat"
