"""Sensor file for Elvia."""

from typing import Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER, TARIFFTYPES_PATH
from .coordinator import ElviaDataUpdateCoordinator

TARIFFTYPE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="tariffKey",
        name="Tarifftype Tariff key",
    ),
    SensorEntityDescription(
        key="product",
        name="Tarifftype Product",
    ),
    SensorEntityDescription(
        key="companyName",
        name="Tarifftype Company name",
    ),
    SensorEntityDescription(
        key="title",
        name="Tarifftype Title",
    ),
    SensorEntityDescription(
        key="consumptionFlag",
        name="Tarifftype Consumption flag",
    ),
    SensorEntityDescription(
        key="lastUpdated",
        name="Tarifftype Last updated",
    ),
    SensorEntityDescription(
        key="usePublicHolidayPrices",
        name="Tarifftype Public Holiday Prices",
    ),
    SensorEntityDescription(
        key="useWeekendPrices",
        name="Tarifftype Weekend Prices",
    ),
    SensorEntityDescription(
        key="resolution",
        name="Tarifftype Resolution",
    ),
)

FIXED_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="monthlyTotal",
        name="Fixed Price Monthly total",
    ),
    SensorEntityDescription(
        key="monthlyTotalExVat",
        name="Fixed Price Monthly total ex vat",
    ),
    SensorEntityDescription(
        key="monthlyExTaxes",
        name="Fixed Price Monthly ex taxes",
    ),
    SensorEntityDescription(
        key="monthlyTaxes",
        name="Fixed Price Monthly taxes",
    ),
    SensorEntityDescription(
        key="monthlyUnitOfMeasure",
        name="Fixed Price Monthly unit of measure",
    ),
    SensorEntityDescription(
        key="levelInfo",
        name="Fixed Price Level info",
    ),
    SensorEntityDescription(
        key="currency",
        name="Fixed Price Currency",
    ),
    SensorEntityDescription(
        key="monetaryUnitOfMeasure",
        name="Fixed Price Monetary unit of measure",
    ),
)

FIXED_HOUR_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="total",
        name="Fixed Price Total",
    ),
    SensorEntityDescription(
        key="totalExVat",
        name="Fixed Price Total ex vat",
    ),
)

ENERGY_PRICE_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="season",
        name="Energy Price Season",
    ),
    SensorEntityDescription(
        key="level",
        name="Energy Price Level",
    ),
    SensorEntityDescription(
        key="total",
        name="Energy Price Total",
    ),
    SensorEntityDescription(
        key="totalExVat",
        name="Energy Price Total ex vat",
    ),
    SensorEntityDescription(
        key="energyExTaxes",
        name="Energy Price Energy ex taxes",
    ),
    SensorEntityDescription(
        key="taxes",
        name="Energy Price Taxes",
    ),
    SensorEntityDescription(
        key="currency",
        name="Energy Price Currency",
    ),
    SensorEntityDescription(
        key="monetaryUnitOfMeasure",
        name="Energy Price Monetary unit of measure",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensor entities from a config_entry."""

    coordinator: ElviaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(ElviaTariffTypeSensor(coordinator, description, "tarifftype") for description in TARIFFTYPE_SENSORS)
    async_add_entities(ElviaFixedPriceSensor(coordinator, description, "fixed_price") for description in FIXED_PRICE_SENSORS)
    async_add_entities(ElviaFixedHourPriceSensor(coordinator, description, "fixed_hour_price") for description in FIXED_HOUR_PRICE_SENSORS)
    async_add_entities(ElviaEnergyPriceSensor(coordinator, description, "energy_price") for description in ENERGY_PRICE_SENSORS)

class ElviaSensor(CoordinatorEntity, SensorEntity):
    """Define a Elvia entity."""

    coordinator: ElviaDataUpdateCoordinator
    sensor_data: Any
    attribute: str

    def __init__(
        self,
        coordinator: ElviaDataUpdateCoordinator,
        description: SensorEntityDescription,
        key_prefix: str
    ) -> None:
        """Initialize."""

        description.key = f"{key_prefix}_{description.key}"

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self.attribute = self.entity_description.key.replace(f"{key_prefix}_", "")
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self.update_from_data()

    @property
    def native_value(self) -> StateType:
        """Return the state."""
        return cast(StateType, self.sensor_data)

    def update_from_data(self) -> None:
        self.sensor_data = "unknown"

    @callback
    def _handle_coordinator_update(self) -> None:
        self.update_from_data()
        super()._handle_coordinator_update()


class ElviaTariffTypeSensor(ElviaSensor):
    """Define a ElviaTariffTypeSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.tariffType.__getattribute__(self.attribute) if (self.coordinator.tariffType is not None) else "unknown"

class ElviaFixedPriceSensor(ElviaSensor):
    """Define a ElviaFixedPriceSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.priceLevel.__getattribute__(self.attribute) if (self.coordinator.priceLevel is not None) else "unknown"

class ElviaFixedHourPriceSensor(ElviaSensor):
    """Define a ElviaFixedHourPriceSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.hourPrice.__getattribute__(self.attribute) if (self.coordinator.hourPrice is not None) else "unknown"

class ElviaEnergyPriceSensor(ElviaSensor):
    """Define a ElviaEnergyPriceSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.energyPrice.__getattribute__(self.attribute) if (self.coordinator.energyPrice is not None) else "unknown"
