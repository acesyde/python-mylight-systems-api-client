import aioresponses
import pytest

from mylightsystems import MyLightSystemsApiClient
from mylightsystems.exceptions import MyLightSystemsError
from tests import load_fixture
from tests.const import MOCK_URL

_AUTH_URL = f"{MOCK_URL}/api/auth"


@pytest.mark.parametrize(
    "status",
    [400, 404, 500],
)
async def test_login_return_non_2xx_status_code_raise_error(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
    status: int,
) -> None:
    """Test status call."""
    responses.get(
        _AUTH_URL,
        status=status,
        body=load_fixture("login.json"),
    )
    with pytest.raises(MyLightSystemsError):
        await client.login(email="fake", password="fake")


async def test_login_success_return_token(
    responses: aioresponses,
    client: MyLightSystemsApiClient,
) -> None:
    """Test login call."""
    responses.get(
        _AUTH_URL,
        status=200,
        payload=load_fixture("login.json"),
    )
    response = await client.login(email="fake", password="fake")
    assert response is not None
    assert response.token == "fake-token"
