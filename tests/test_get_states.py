"""Tests for get states."""

import pytest
from aioresponses import aioresponses
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
async def test_get_states__should_raise_error_when_non_2xx_status_code(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test that non-2xx status codes raise MyLightSystemsError."""
    # Given
    responses.get(
        f"{_STATES_URL}?authToken=fake-token",
        status=status,
    )

    # When / Then
    with pytest.raises(MyLightSystemsError):
        await client.get_states(auth_token="fake-token")


async def test_get_states__should_raise_unauthorized_error_when_bad_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that bad token raises MyLightSystemsUnauthorizedError."""
    # Given
    responses.get(
        f"{_STATES_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_states(auth_token="fake-token")


async def test_get_states__should_return_states_when_valid_request(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that valid request returns states data."""
    # Given
    responses.get(
        f"{_STATES_URL}?authToken=fake-token",
        status=200,
        body=load_fixture("states.json"),
    )

    # When
    response = await client.get_states(auth_token="fake-token")

    # Then
    assert response is not None
    assert 8 == len(response)

    device_state = response[0]
    assert isinstance(device_state, DeviceState)
    assert "F7DFE301A82C" == device_state.device_id
    assert 150 == device_state.report_period
    assert not device_state.state
    assert 1 == len(device_state.sensor_states)
    sensor_state = device_state.sensor_states[0]
    assert isinstance(sensor_state, SensorState)
    assert "F7DFE301A82C-pow" == sensor_state.sensor_id
    assert "2024-07-28 18:03:14" == sensor_state.measure.date
    assert "watt" == sensor_state.measure.unit
    assert "electric_power" == sensor_state.measure.type
    assert 0.0 == sensor_state.measure.value
