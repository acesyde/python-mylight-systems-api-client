"""Tests for get devices."""

from aioresponses import aioresponses
import pytest

from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)
from mylightsystems.models import (
    BatteryDevice,
    CompositeCounterDevice,
    CounterDevice,
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

    device = response[0]
    assert isinstance(device, RelayDevice)
    assert device.id == "4D9F3281C75E"
    assert device.name == "Relais"
    assert device.type == "sw"
    assert device.master_id == "F8DFE101A81C"
    assert device.master_type == "mst"

    device = response[1]
    assert isinstance(device, CounterDevice)
    assert device.id == "B2F7E9A1C75E"
    assert device.name == "Consommation"
    assert device.type == "cmp"
    assert device.master_id == "4D9F3081C75E"
    assert device.master_type == "gmd"

    device = response[4]
    assert isinstance(device, CompositeCounterDevice)
    assert device.id == "4D9F3081C75E"
    assert device.name == "Compteur"
    assert device.type == "gmd"
    assert len(device.children) == 3
    assert device.master_id == "F8DFE101A81C"
    assert device.master_type == "mst"

    device = response[5]
    assert isinstance(device, MasterDevice)
    assert device.id == "F8DFE101A81C"
    assert device.name == "Master"
    assert device.type == "mst"
    assert device.type_id == "asoka_red_plug"
    assert device.state
    assert device.report_period == 300

    device = response[6]
    assert isinstance(device, VirtualDevice)
    assert device.id == "E9C5FA81C75E"
    assert device.name == "Virtual 1"
    assert device.type == "vrt"
    assert device.type_id == "virtual"
    assert not device.state

    device = response[7]
    assert isinstance(device, BatteryDevice)
    assert device.id == "E9BC5FA11C75E"
    assert device.name == "Battery 1"
    assert device.type == "bat"
    assert device.capacity == 100
    assert device.state
