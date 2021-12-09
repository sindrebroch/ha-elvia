"""Elvia data coordinator."""

from datetime import timedelta, datetime

from aiohttp.client_exceptions import ClientConnectorError
from voluptuous.error import Error

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ElviaApiClient
from .const import DATE_FORMAT, DOMAIN, LOGGER
from .models import GridTariffCollection, TariffType, PriceInfo, PriceLevel, VariablePrice

class ElviaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching from Elvia data API."""
    
    nextFetch: datetime

    data: GridTariffCollection
    hourlyPriceInfo: PriceInfo
    fixedPriceLevel: PriceLevel
    variablePrice: VariablePrice
    
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
            manufacturer=self.device_info.company,
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

        now = datetime.now()

        if self.nextFetch is None or self.nextFetch < now:
            return self.data

        try:
            meteringpoint = await self.api.meteringpoint()

            for hourlyPriceInfo in meteringpoint.gridTariff.tariffPrice.priceInfo:

                start = datetime.strptime(hourlyPriceInfo.startTime[0:19], DATE_FORMAT)
                end = datetime.strptime(hourlyPriceInfo.expiredAt[0:19], DATE_FORMAT)

                if (now < start) and (now > end):
                    continue

                self.hourlyPriceInfo = hourlyPriceInfo
                
                for fixedPrice in hourlyPriceInfo.fixedPrices:      # TODO handle multiple?
                    for priceLevel in fixedPrice.priceLevels:       # TODO handle multiple?
                        self.fixedPriceLevel = priceLevel

                self.variablePrice = hourlyPriceInfo.variablePrice
                self.nextFetch = now + timedelta(hours=1) # TODO be more specific to refresh at new hour

            return meteringpoint
        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

        ## priceinfo -- list
        # startTime: str
        # expiredAt: str
        # hoursShortName: str
        # season: str
        # publicHoliday: bool
        # fixedPrices: List[FixedPrices]
        # variablePrice: VariablePrice

        ## fixedprices
        # priceLevel: List[PriceLevel]