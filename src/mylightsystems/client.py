"""Client for MyLightSystems API."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
import socket
from typing import TYPE_CHECKING, Any

from aiohttp import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from mylightsystems.const import AUTH_URL, DEFAULT_BASE_URL, PROFILE_URL
from mylightsystems.exceptions import (
    MyLightSystemsConnectionError,
    MyLightSystemsInvalidAuthError,
    MyLightSystemsUnauthorizedError,
)
from mylightsystems.models import Login, Profile

if TYPE_CHECKING:
    from typing_extensions import Self

_LOGGER = logging.getLogger(__name__)


@dataclass
class MyLightSystemsApiClient:
    """Main class for handling communication with MyLightSystems API."""

    base_url: str = DEFAULT_BASE_URL
    session: ClientSession | None = None
    request_timeout: int = 10
    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the MyLightSystems API."""
        url = URL(self.base_url).with_path(uri)

        headers = {
            "Content-Type": "application/json",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method, url, headers=headers, params=params
                )

                _LOGGER.debug(
                    "Data retrieved from %s, status: %s", url, response.status
                )

                response.raise_for_status()

                json_response = await response.json()

                if (
                    json_response["status"] == "error"
                    and json_response["error"] == "not.authorized"
                ):
                    raise MyLightSystemsUnauthorizedError

                return json_response

        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the device"
            raise MyLightSystemsConnectionError(msg) from exception
        except (
            ClientError,
            ClientResponseError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating with the device"
            raise MyLightSystemsConnectionError(msg) from exception

    async def login(self, email: str, password: str) -> Login:
        """Login to MyLightSystems API."""
        response = await self._request(
            AUTH_URL,
            params={"email": email, "password": password},
        )

        if response["status"] == "error" and response["error"] in (
            "invalid.credentials",
            "undefined.email",
            "undefined.password",
        ):
            raise MyLightSystemsInvalidAuthError

        return Login(token=response["authToken"])

    async def get_profile(self, auth_token: str) -> Profile:
        """Get user profile."""
        response = await self._request(
            PROFILE_URL,
            params={"authToken": auth_token},
        )

        return Profile(id=response["id"], grid_type=response["gridType"])

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The AirGradientClient object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
