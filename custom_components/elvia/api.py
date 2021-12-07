"""Asynchronous Python client for Elvia."""

from typing import Any, Dict

import socket
import asyncio
import urllib.parse
import aiohttp
import async_timeout
from aiohttp.client import ClientSession

from .const import API_HEADERS, LOGGER, METERINGPOINT_PATH, PING_PATH, SECURE_PATH, TARIFFQUERY_PATH, TARIFFTYPE_PATH


class ApiClientException(Exception):
    """Api Client Exception."""


class ElviaApiClient:
    """Main class for handling connections with a Elvia unit."""

    def __init__(
        self,
        session: ClientSession,
        api_key: str,
        metering_point_id: str
    ) -> None:
        """Initialize connection with the Elvia."""
        self._session = session
        self._api_key = api_key
        self._metering_point_id = metering_point_id

    async def get(self, url: str) -> Any:
        """Get request."""
        return await self.api_wrapper(
            method="GET",
            url=url,
            headers=self.headers_with_api_key(),
        )

    async def post(self, url: str, data: dict[str, Any]= {}) -> Any:
        """Post request."""
        return await self.api_wrapper(
            method="POST",
            url=url,
            headers=self.headers_with_api_key(),
            data=data
        )

    async def api_wrapper(
        self,
        method: str,
        url: str,
        data: dict[str, Any] = {},
        headers: dict = {},
    ) -> dict[str, Any] or None:
        """Wrap request."""

        LOGGER.debug(
            "%s-request to url=%s. data=%s. headers=%s",
            method,
            url,
            data,
            headers,
        )

        try:
            async with async_timeout.timeout(10, loop=asyncio.get_event_loop()):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                )
                return await response.json()
        except asyncio.TimeoutError as exception:
            raise ApiClientException(
                f"Timeout error fetching information from {url}"
            ) from exception
        except (KeyError, TypeError) as exception:
            raise ApiClientException(
                f"Error parsing information from {url} - {exception}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ApiClientException(
                f"Error fetching information from {url} - {exception}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ApiClientException(exception) from exception

    async def ping(self) -> bool:
        """Ping endpoint."""
        return await self.get(PING_PATH)

    async def secure(self) -> bool:
        """Secure endpoint."""
        return await self.get(SECURE_PATH)

    async def tariff_type(self):
        """Get all available private tariff types."""
        return await self.get(TARIFFTYPE_PATH)

    async def tariff_query(self):
        """Get tariff data/prices for a given tariff for a given timeperiod."""
        return await self.get(TARIFFQUERY_PATH)

    async def meteringpoint(self):
        """Returns tariff(s) and MPID(s) for the MPIDs(MeteringpointId/Målepunkt-Id) given as input."""
        return await self.post(METERINGPOINT_PATH)

    def headers_with_api_key(self) -> Dict[str, str]:
        """Get headers with api_key added."""
        assert self._api_key is not None
        return {**API_HEADERS, **{"Ocp-Apim-Subscription-Key": f"{self._api_key}"}}