"""Tests for get profile."""

from aioresponses import aioresponses
import pytest

from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)
from mylightsystems.models import DeviceState, SensorState
from tests import load_fixture
from tests.const import MOCK_URL

_STATES_URL = f"{MOCK_URL}/api/states"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_get_states_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        f"{_STATES_URL}?authToken=fake-token",
        status=status,
    )
    with pytest.raises(MyLightSystemsError):
        await client.get_states(auth_token="fake-token")


async def test_get_states_with_bad_token_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad token call."""
    responses.get(
        f"{_STATES_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_states(auth_token="fake-token")


async def test_get_states_success_return_measures(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test get profile call."""
    responses.get(
        f"{_STATES_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("states.json"),
    )
    response = await client.get_states(auth_token="fake-token")
    assert response is not None
    assert len(response) == 8

    device_state = response[0]
    assert isinstance(device_state, DeviceState)
    assert device_state.device_id == "F7DFE301A82C"
    assert device_state.report_period == 150
    assert not device_state.state
    assert len(device_state.sensor_states) == 1
    sensor_state = device_state.sensor_states[0]
    assert isinstance(sensor_state, SensorState)
    assert sensor_state.sensor_id == "F7DFE301A82C-pow"
    assert sensor_state.measure.date == "2024-07-28 18:03:14"
    assert sensor_state.measure.unit == "watt"
    assert sensor_state.measure.type == "electric_power"
    assert sensor_state.measure.value == 0.0
