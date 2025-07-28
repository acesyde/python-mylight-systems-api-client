"""Tests for get devices."""

import pytest
from aioresponses import aioresponses
from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)
from mylightsystems.models import (
    BatteryDevice,
    CompositeCounterDevice,
    CounterDevice,
    EthernetDevice,
    MasterDevice,
    RelayDevice,
    VirtualDevice,
)

from tests import load_fixture
from tests.const import MOCK_URL

_DEVICE_URL = f"{MOCK_URL}/api/devices"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_get_devices__should_raise_error_when_non_2xx_status_code(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test that get_devices raises MyLightSystemsError when API returns non-2xx status code."""
    # Given
    token = "fake-token"

    # When
    responses.get(
        str(f"{_DEVICE_URL}?authToken={token}"),
        status=status,
    )

    # Then
    with pytest.raises(MyLightSystemsError):
        await client.get_devices(auth_token=token)


async def test_get_devices__should_raise_unauthorized_error_when_bad_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that get_devices raises MyLightSystemsUnauthorizedError when using invalid token."""
    # Given
    token = "fake-token"

    # When
    responses.get(
        str(f"{_DEVICE_URL}?authToken={token}"),
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    # Then
    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_devices(auth_token=token)


async def test_get_devices__should_return_devices_when_valid_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that get_devices returns properly parsed device list when using valid token."""
    # Given
    token = "fake-token"

    # When
    responses.get(
        str(f"{_DEVICE_URL}?authToken={token}"),
        status=200,
        body=load_fixture("devices.json"),
    )
    response = await client.get_devices(auth_token=token)

    # Then
    assert response is not None
    assert 9 == len(response)

    device = response[0]
    assert isinstance(device, EthernetDevice)
    assert "E9C5FA81C75F" == device.id
    assert "Ordinateur" == device.name
    assert "Ordinateur" == device.device_type_name
    assert "eth" == device.type
    assert "mst" == device.master_type

    device = response[1]
    assert isinstance(device, RelayDevice)
    assert "4D9F3281C75E" == device.id
    assert "Relais" == device.name
    assert "sw" == device.type
    assert "F8DFE101A81C" == device.master_id
    assert "mst" == device.master_type

    device = response[2]
    assert isinstance(device, CounterDevice)
    assert "B2F7E9A1C75E" == device.id
    assert "Consommation" == device.name
    assert "cmp" == device.type
    assert "4D9F3081C75E" == device.master_id
    assert "gmd" == device.master_type

    device = response[5]
    assert isinstance(device, CompositeCounterDevice)
    assert "4D9F3081C75E" == device.id
    assert "Compteur" == device.name
    assert "gmd" == device.type
    assert 3 == len(device.children)
    assert "F8DFE101A81C" == device.master_id
    assert "mst" == device.master_type

    device = response[6]
    assert isinstance(device, MasterDevice)
    assert "F8DFE101A81C" == device.id
    assert "Master" == device.name
    assert "mst" == device.type
    assert "asoka_red_plug" == device.type_id
    assert device.state
    assert 300 == device.report_period

    device = response[7]
    assert isinstance(device, VirtualDevice)
    assert "E9C5FA81C75E" == device.id
    assert "Virtual 1" == device.name
    assert "vrt" == device.type
    assert "virtual" == device.type_id
    assert not device.state

    device = response[8]
    assert isinstance(device, BatteryDevice)
    assert "E9BC5FA11C75E" == device.id
    assert "Battery 1" == device.name
    assert "bat" == device.type
    assert 100 == device.capacity
    assert device.state
