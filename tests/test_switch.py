"""Tests for switch."""

import pytest
from aioresponses import aioresponses
from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)
from mylightsystems.exceptions import (
    MyLightSystemsSwitchNotAllowedError,
    MyLightSystemsUnknownDeviceError,
)
from mylightsystems.models import SwitchState

from tests import load_fixture
from tests.const import MOCK_URL

_SWITCH_URL = f"{MOCK_URL}/api/device/switch"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_switch__should_raise_error_when_non_2xx_status_code(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test that non-2xx status codes raise MyLightSystemsError."""
    # Given
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=status,
    )

    # When / Then
    with pytest.raises(MyLightSystemsError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch__should_raise_unauthorized_error_when_bad_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that bad token raises MyLightSystemsUnauthorizedError."""
    # Given
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch__should_raise_not_allowed_error_when_not_allowed(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that not allowed operation raises MyLightSystemsSwitchNotAllowedError."""
    # Given
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=200,
        body=load_fixture("switch_not_allowed.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsSwitchNotAllowedError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch__should_raise_unknown_device_error_when_unknown_device(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that unknown device raises MyLightSystemsUnknownDeviceError."""
    # Given
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=200,
        body=load_fixture("switch_device_not_found.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsUnknownDeviceError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch__should_return_switch_state_when_valid_request(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that valid request returns switch state."""
    # Given
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=true",
        status=200,
        body=load_fixture("switch.json"),
    )

    # When
    response = await client.switch(auth_token="fake-token", device_id="test", value=True)

    # Then
    assert response is not None
    assert isinstance(response, SwitchState)
    assert response.state
