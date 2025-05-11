"""Asynchronous Python client for MyLightSystems."""

from collections.abc import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from mylightsystems import MyLightSystemsApiClient
from tests.const import MOCK_URL


@pytest.fixture
async def client() -> AsyncGenerator[MyLightSystemsApiClient]:
    """Return a MyLightSustems client."""
    async with (
        aiohttp.ClientSession() as session,
        MyLightSystemsApiClient(
            MOCK_URL,
            session=session,
        ) as mylightsystems_client,
    ):
        yield mylightsystems_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
