"""Tests for get measures total."""

import pytest
from aioresponses import aioresponses
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
async def test_get_measures_total__should_raise_error_when_non_2xx_status_code(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test that non-2xx status codes raise MyLightSystemsError."""
    # Given
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=status,
    )

    # When / Then
    with pytest.raises(MyLightSystemsError):
        await client.get_measures_total(auth_token="fake-token", device_id="a")


async def test_get_measures_total__should_raise_unauthorized_error_when_bad_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that bad token raises MyLightSystemsUnauthorizedError."""
    # Given
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=200,
        body=load_fixture("unauthorized.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsUnauthorizedError):
        await client.get_measures_total(auth_token="fake-token", device_id="a")


async def test_get_measures_total__should_raise_not_supported_error_when_unsupported_device(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that unsupported device raises MyLightSystemsMeasuresTotalNotSupportedError."""
    # Given
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=200,
        body=load_fixture("measures_total_unsupported.json"),
    )

    # When / Then
    with pytest.raises(MyLightSystemsMeasuresTotalNotSupportedError):
        await client.get_measures_total(auth_token="fake-token", device_id="a")


async def test_get_measures_total__should_return_measures_when_valid_request(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test that valid request returns measures data."""
    # Given
    responses.get(
        f"{_MEASURES_TOTAL_URL}?authToken=fake-token&device_id=a",
        status=200,
        body=load_fixture("measures_total.json"),
    )

    # When
    response = await client.get_measures_total(auth_token="fake-token", device_id="a")

    # Then
    assert response is not None
    assert 2 == len(response)

    measure = response[0]
    assert isinstance(measure, Measure)
    assert "power" == measure.type
    assert "W" == measure.unit
    assert 97277207.27799994 == measure.value
