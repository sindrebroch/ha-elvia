"""Elvia data coordinator."""

from typing import Any

from time import localtime
from datetime import timedelta, datetime

from aiohttp.client_exceptions import ClientConnectorError
from voluptuous.error import Error

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ElviaApiClient
from .const import DOMAIN, LOGGER
from .models import EnergyPrice, GridTariffCollection, HourPrice, PriceLevel, TariffType


class ElviaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching from Elvia data API."""


    last_hour_fetched: int or None = None

    tariffType: TariffType or None = None
    priceLevel: PriceLevel or None = None
    hourPrice: HourPrice or None = None
    energyPrice: EnergyPrice or None = None

    forbruksledd: float or None = None
    kapasitetsledd: float or None = None
    level_info: str or None = None
    fixed_price: int or None = None

    maxhours: Any or None = None
    mapped_maxhours: Any or None = None
    meteringpoint: GridTariffCollection

    def __init__(
        self,
        hass: HomeAssistant,
        api: ElviaApiClient,
        tariffType: TariffType,
    ) -> None:
        """Initialize."""

        self.api = api
        self.device_info = tariffType

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
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self) -> GridTariffCollection:
        """Update data via library."""

        # Only update values once every hour, at the start of the hour.
        current_hour = datetime.now().time().hour
        if current_hour == self.last_hour_fetched:
            return
        else:
            self.last_hour_fetched = current_hour

        try:
            self.meteringpoint = await self.api.meteringpoint()
            self.maxhours = await self.api.maxhours()

            await self.map_meteringpoint_values(self.meteringpoint)
            await self.map_maxhour_values(self.maxhours)

            return {
                'meteringpoint': self.meteringpoint,
                'maxhours': self.maxhours,
            }
        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

    async def map_maxhour_values(self, data) -> None:
        aggregates = data['meteringpoints'][0]['maxHoursAggregate']

        self.mapped_maxhours = {}

        for aggregateMonth in aggregates:
            if aggregateMonth['noOfMonthsBack'] == 0:
                self.mapped_maxhours["current_month"] = {
                    "3": {
                        "value": aggregateMonth['maxHours'][0]['value'],
                        "startTime": aggregateMonth['maxHours'][0]['startTime'],
                        "endTime": aggregateMonth['maxHours'][0]['endTime'],
                        "uom": aggregateMonth['maxHours'][0]['uom'],
                    },
                    "2": {
                        "value": aggregateMonth['maxHours'][1]['value'],
                        "startTime": aggregateMonth['maxHours'][1]['startTime'],
                        "endTime": aggregateMonth['maxHours'][1]['endTime'],
                        "uom": aggregateMonth['maxHours'][1]['uom'],
                    },
                    "1": {
                        "value": aggregateMonth['maxHours'][2]['value'],
                        "startTime": aggregateMonth['maxHours'][2]['startTime'],
                        "endTime": aggregateMonth['maxHours'][2]['endTime'],
                        "uom": aggregateMonth['maxHours'][2]['uom'],
                    },
                    "average": aggregateMonth['averageValue'],
                    "uom": aggregateMonth['uom']
                }
            elif aggregateMonth['noOfMonthsBack'] == 1:
                self.mapped_maxhours["previous_month"] = {
                    "3": {
                        "value": aggregateMonth['maxHours'][0]['value'],
                        "startTime": aggregateMonth['maxHours'][0]['startTime'],
                        "endTime": aggregateMonth['maxHours'][0]['endTime'],
                        "uom": aggregateMonth['maxHours'][0]['uom'],
                    },
                    "2": {
                        "value": aggregateMonth['maxHours'][1]['value'],
                        "startTime": aggregateMonth['maxHours'][1]['startTime'],
                        "endTime": aggregateMonth['maxHours'][1]['endTime'],
                        "uom": aggregateMonth['maxHours'][1]['uom'],
                    },
                    "1": {
                        "value": aggregateMonth['maxHours'][2]['value'],
                        "startTime": aggregateMonth['maxHours'][2]['startTime'],
                        "endTime": aggregateMonth['maxHours'][2]['endTime'],
                        "uom": aggregateMonth['maxHours'][2]['uom'],
                    },
                    "average": aggregateMonth['averageValue'],
                    "uom": aggregateMonth['uom']
                }

    async def map_meteringpoint_values(self, data) -> None:
        """Map values."""

        current_datetime = datetime.now()

        zoneadjust = "+02:00" if localtime().tm_isdst > 0 else "+01:00"

        pretty_now = (
            str(current_datetime.year)
            + "-"
            + str(current_datetime.month).zfill(2)
            + "-"
            + str(current_datetime.day).zfill(2)
            + "T"
            + str(current_datetime.hour).zfill(2)
            + ":"
            + str(current_datetime.minute).zfill(2)
            + ":"
            + str(current_datetime.second).zfill(2)
            + zoneadjust
        )

        today_string = (
            str(current_datetime.year)
            + "-"
            + str(current_datetime.month).zfill(2)
            + "-"
            + str(current_datetime.day).zfill(2)
        )

        self.tariffType = data.gridTariff.tariffType

        tariff_price = data.gridTariff.tariffPrice

        first_metering_point = next(data.meteringPointsAndPriceLevels)
        fixed_price_level_id = first_metering_point.currentFixedPriceLevel.levelId

        for hour in tariff_price.hours:
            start_time = hour.startTime
            end_time = hour.expiredAt
            value = hour.energyPrice.total

            if start_time[0:10] == today_string:
                if (pretty_now >= start_time) and (pretty_now < end_time):
                    variable_price_per_hour = value
                    for_loop_break = False

                    for fixed_price_element in tariff_price.priceInfo.fixedPrices:
                        if hour.fixedPrice.id == fixed_price_element.id:
                            for price_levels_element in fixed_price_element.priceLevels:
                                if price_levels_element.id == fixed_price_level_id:
                                    hour_prices = next(price_levels_element.hourPrices)
                                    fixed_price_per_hour = hour_prices.total
                                    fixed_price_level_info = (
                                        price_levels_element.levelInfo
                                    )
                                    fixed_price = price_levels_element.monthlyTotal
                                    for_loop_break = True
                                    break
                            if for_loop_break is True:
                                self.kapasitetsledd = fixed_price_per_hour
                                self.forbruksledd = variable_price_per_hour
                                self.level_info = fixed_price_level_info
                                self.fixed_price = fixed_price
                                break
