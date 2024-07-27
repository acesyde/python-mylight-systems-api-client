"""Asynchronous Python client for AirGradient."""

from typing import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from mylightsystems import MyLightSystemsApiClient
from tests.const import MOCK_URL


@pytest.fixture
async def client() -> AsyncGenerator[MyLightSystemsApiClient, None]:
    """Return a MyLightSustems client."""
    async with aiohttp.ClientSession() as session, MyLightSystemsApiClient(
        MOCK_URL,
        session=session,
    ) as mylightsystems_client:
        yield mylightsystems_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
