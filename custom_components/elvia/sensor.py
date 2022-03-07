"""Sensor file for Elvia."""

from typing import Any, Optional, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import ElviaDataUpdateCoordinator

FIXED_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="fixed_price_level",
        name="Fixed pricelevel",
        icon="mdi:currency-usd",
    ),
)
FIXED_PRICE_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="fixed_price_total",
        name="Price fixed total",
        icon="mdi:currency-usd",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="fixed_price_fixed",
        name="Price fixed",
        icon="mdi:currency-usd",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="fixed_price_taxes",
        name="Price fixed taxes",
        icon="mdi:currency-usd",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

VARIABLE_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="variable_price_power",
        name="Variable power",
        icon="mdi:currency-usd",
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="variable_price_level",
        name="Variable pricelevel",
        icon="mdi:currency-usd",
    ),
)
VARIABLE_PRICE_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="variable_price_total",
        name="Price variable total",
        icon="mdi:currency-usd",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="variable_price_taxes",
        name="Price variable taxes",
        icon="mdi:currency-usd",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="variable_price_energy",
        name="Price variable energy",
        icon="mdi:currency-usd",
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensor entities from a config_entry."""

    coordinator: ElviaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities(ElviaFixedPriceSensor(coordinator, description) for description in FIXED_PRICE_SENSORS)
    async_add_entities(ElviaFixedPricePriceSensor(coordinator, description) for description in FIXED_PRICE_PRICE_SENSORS)
    async_add_entities(ElviaVariablePriceSensor(coordinator, description) for description in VARIABLE_PRICE_SENSORS)
    async_add_entities(ElviaVariablePricePriceSensor(coordinator, description) for description in VARIABLE_PRICE_PRICE_SENSORS)


class ElviaSensor(CoordinatorEntity, SensorEntity):
    """Define a Elvia entity."""

    coordinator: ElviaDataUpdateCoordinator
    sensor_data: Any

    def __init__(
        self,
        coordinator: ElviaDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self.update_from_data()

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    def update_from_data(self) -> None:

        self.sensor_data = ""

    @callback
    def _handle_coordinator_update(self) -> None:

        self.update_from_data()
        super()._handle_coordinator_update()

class ElviaVariablePriceSensor(ElviaSensor):

    def update_from_data(self) -> None:
        key = self.entity_description.key
        variablePrice = self.coordinator.variablePrice
        attribute = key.replace("variable_price_", "")

        self.sensor_data = variablePrice.__getattribute__(attribute)

class ElviaVariablePricePriceSensor(ElviaSensor):

    def update_from_data(self) -> None:
        key = self.entity_description.key
        variablePrice = self.coordinator.variablePrice
        attribute = key.replace("variable_price_", "")

        self.sensor_data = float(variablePrice.__getattribute__(attribute))

    @property
    def native_unit_of_measurement(self) -> str or None:
        """Return the unit of measurement of the sensor, if any."""
        return self.coordinator.variablePrice.uom

class ElviaFixedPriceSensor(ElviaSensor):

    def update_from_data(self) -> None:
        key = self.entity_description.key
        priceLevel = self.coordinator.fixedPriceLevel
        attribute = key.replace("fixed_price_", "")

        self.sensor_data = priceLevel.__getattribute__(attribute)

class ElviaFixedPricePriceSensor(ElviaSensor):

    def update_from_data(self) -> None:

        key = self.entity_description.key
        priceLevel = self.coordinator.fixedPriceLevel
        attribute = key.replace("fixed_price_", "")

        self.sensor_data = float(priceLevel.__getattribute__(attribute))

    @property
    def native_unit_of_measurement(self) -> str or None:
        """Return the unit of measurement of the sensor, if any."""

        return self.coordinator.fixedPriceLevel.uom
