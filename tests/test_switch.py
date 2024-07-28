"""Tests for get profile."""

from aioresponses import aioresponses
import pytest

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
async def test_switch_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=status,
    )
    with pytest.raises(MyLightSystemsError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch_with_bad_token_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad token call."""
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch_with_not_allowed_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test not allowed call."""
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=200,
        body=load_fixture("switch_not_allowed.json"),
    )

    with pytest.raises(MyLightSystemsSwitchNotAllowedError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch_with_unknown_device_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test unknown device call."""
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=false",
        status=200,
        body=load_fixture("switch_device_not_found.json"),
    )

    with pytest.raises(MyLightSystemsUnknownDeviceError):
        await client.switch(auth_token="fake-token", device_id="test", value=False)


async def test_switch_success_return_profile(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test switch call."""
    responses.get(
        f"{_SWITCH_URL}?authToken=fake-token&id=test&on=true",
        status=200,
        body=load_fixture("switch.json"),
    )
    response = await client.switch(
        auth_token="fake-token", device_id="test", value=True
    )
    assert response is not None
    assert isinstance(response, SwitchState)
    assert response.state
