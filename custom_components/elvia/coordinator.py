"""Elvia data coordinator."""

from datetime import timedelta, datetime

from aiohttp.client_exceptions import ClientConnectorError
from voluptuous.error import Error

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ElviaApiClient
from .const import DATE_FORMAT, DOMAIN, LOGGER
from .models import EnergyPrice, GridTariffCollection, HourPrice, PriceLevel, TariffType

class ElviaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching from Elvia data API."""

    nextFetch: datetime

    data: GridTariffCollection

    tariffType: TariffType or None = None
    priceLevel: PriceLevel or None = None
    hourPrice: HourPrice or None = None
    energyPrice: EnergyPrice or None = None

    def __init__(
        self,
        hass: HomeAssistant,
        api: ElviaApiClient,
        update_interval: int,
        tariffType: TariffType,
    ) -> None:
        """Initialize."""

        self.api = api
        self.device_info = tariffType
        self.nextFetch = datetime.now() + timedelta(hours=1)

        self._attr_device_info = DeviceInfo(
            name=self.device_info.title,
            manufacturer=self.device_info.companyName,
            model=self.device_info.tariffKey,
            identifiers={(DOMAIN, self.api._metering_point_id)},
            configuration_url="https://www.elvia.no/logg-inn/",
        )

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    async def _async_update_data(self) -> GridTariffCollection:
        """Update data via library."""

        try:
            response = await self.api.meteringpoint()
            await self.mapValues(response)
            return response
        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

    async def mapValues(self, data) -> None:
        self.tariffType = data.gridTariff.tariffType
        for fixedPrice in data.gridTariff.tariffPrice.priceInfo.fixedPrices:
            for priceLevel in fixedPrice.priceLevels:
                self.priceLevel = priceLevel
                for hourPrice in self.priceLevel.hourPrices:
                    self.hourPrice = hourPrice
        for energyPrice in data.gridTariff.tariffPrice.priceInfo.energyPrices:
            self.energyPrice = energyPrice
