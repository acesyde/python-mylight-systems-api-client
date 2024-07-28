"""Tests for get profile."""

from aioresponses import aioresponses
import pytest

from mylightsystems import (
    MyLightSystemsApiClient,
    MyLightSystemsError,
    MyLightSystemsUnauthorizedError,
)
from mylightsystems.exceptions import MyLightSystemsMeasuresTotalNotSupportedError
from mylightsystems.models import Measure
from tests import load_fixture
from tests.const import MOCK_URL

_MEASURES_TOTAL_URL = f"{MOCK_URL}/api/measures/total"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_get_measures_total_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=status,
    )
    with pytest.raises(MyLightSystemsError):
        await client.get_measures_total(auth_token="fake-token", device_id="a")


async def test_get_measures_total_with_bad_token_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad token call."""
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_measures_total(auth_token="fake-token", device_id="a")


async def test_get_measures_total_with_unsupported_device_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test bad token call."""
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=200,
        body=load_fixture("measures_total_unsupported.json"),
    )

    with pytest.raises(MyLightSystemsMeasuresTotalNotSupportedError):
        await client.get_measures_total(auth_token="fake-token", device_id="a")


async def test_get_measures_total_success_return_measures(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test get profile call."""
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=200,
        body=load_fixture("measures_total.json"),
    )
    response = await client.get_measures_total(auth_token="fake-token", device_id="a")
    assert response is not None
    assert len(response) == 2

    measure = response[0]
    assert isinstance(measure, Measure)
    assert measure.type == "power"
    assert measure.unit == "W"
    assert measure.value == 97277207.27799994
