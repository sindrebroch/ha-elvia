"""Elvia data coordinator."""

from datetime import timedelta

from aiohttp.client_exceptions import ClientConnectorError
from voluptuous.error import Error

from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ElviaApiClient
from .const import DOMAIN as ELVIA_DOMAIN, LOGGER
from .models import ElviaSensorsResponse


class ElviaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching from Elvia data API."""

    data: ElviaSensorsResponse

    def __init__(
        self,
        hass: HomeAssistant,
        api: ElviaApiClient,
        update_interval: int,
    ) -> None:
        """Initialize."""

        self.api = api
        self.name = "Elvia"

        self._attr_device_info = DeviceInfo(
            name=self.name,
            manufacturer=self.name,
            identifiers={(ELVIA_DOMAIN, self.name)},
        )

        super().__init__(
            hass,
            LOGGER,
            name=ELVIA_DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    async def _async_update_data(self) -> ElviaSensorsResponse:
        """Update data via library."""

        try:
            return await self.api.sensor_data()
        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error
