"""Elvia library."""

from http import HTTPStatus
from typing import Any, Dict, List, Optional

import asyncio
import async_timeout
import aiohttp
import socket

from .const import (
    LOGGER,
    PING_PATH,
    SECURE_PATH,
    TARIFFTYPES_PATH,
    TARIFFQUERY_PATH,
    METERINGPOINT_PATH,
    API_HEADERS,
)
from .models import (
    TariffType,
    GridTariff,
    GridTariffCollection,
)

class ApiClientException(Exception):
    """Api Client Exception."""

class ElviaApiClient:
    """Main class for handling connection with."""

    def __init__(
        self,
        api_key: str,
        metering_point_id: str,
        session: Optional[aiohttp.client.ClientSession] = None,
    ) -> None:
        """Initialize connection with Elvia."""

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
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                )

                # LOGGER.debug("response=%s", response)

                status = response.status
                if status == HTTPStatus.OK:
                    LOGGER.debug("Status 200 OK")
                elif status == HTTPStatus.UNAUTHORIZED: # TODO throw specialized exception
                    LOGGER.debug("Status 401 Unauthorized")
                elif status == HTTPStatus.FORBIDDEN: # TODO throw specialized exception
                    LOGGER.debug("Status 403 Forbidden")
                else:
                    LOGGER.debug("Status=%s", status)

                return await response.json() # TODO does not handle requests without body?
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
        await self.get(PING_PATH)
        return True

    async def secure(self) -> bool:
        """Secure endpoint."""
        return await self.get(SECURE_PATH)

    async def tarifftypes(self) -> List[TariffType]:
        """Get all available private tariff types."""
        return (TariffType.from_dict(tariffType) for tariffType in await self.get(TARIFFTYPES_PATH)["tariffKey"])

    async def tariffquery(self) -> GridTariff:
        """Get tariff data/prices for a given tariff for a given timeperiod."""
        return GridTariff.from_dict(await self.get(TARIFFQUERY_PATH))

    async def meteringpoint(self) -> GridTariffCollection:
        """Returns tariff(s) and MPID(s) for the MPIDs(MeteringpointId/Målepunkt-Id) given as input."""
        response = await self.post(METERINGPOINT_PATH, '{ "meteringPointIds": [ "' + str(self._metering_point_id) + '" ] }')
        for collection in response["gridTariffCollections"]:
            return GridTariffCollection.from_dict(collection)

    def headers_with_api_key(self) -> Dict[str, str]:
        """Get headers with api_key added."""
        assert self._api_key is not None
        return {**API_HEADERS, **{"Ocp-Apim-Subscription-Key": f"{self._api_key}"}}