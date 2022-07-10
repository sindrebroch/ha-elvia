"""Sensor file for Elvia."""

from typing import Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ElviaDataUpdateCoordinator

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="forbruksledd",
        name="Forbruksledd per kWh",
        icon="mdi:currency-usd",
        unit_of_measurement="NOK/kWh",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="kapasitetsledd",
        name="Kapasitetsledd per time",
        icon="mdi:currency-usd",
        unit_of_measurement="NOK/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="level_info",
        name="Fixed price level info",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensor entities from a config_entry."""

    coordinator: ElviaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        ElviaCoordinatorSensor(coordinator, description, "elvia")
        for description in SENSORS
    )


class ElviaSensor(CoordinatorEntity, SensorEntity):
    """Define a Elvia entity."""

    coordinator: ElviaDataUpdateCoordinator
    sensor_data: Any
    attribute: str

    def __init__(
        self,
        coordinator: ElviaDataUpdateCoordinator,
        description: SensorEntityDescription,
        key_prefix: str,
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


class ElviaCoordinatorSensor(ElviaSensor):
    """Define a ElviaTariffTypeSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.__getattribute__(self.attribute)
