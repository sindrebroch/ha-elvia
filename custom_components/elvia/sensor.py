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

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="test",
        name="Test sensor",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensor entities from a config_entry."""

    coordinator: ElviaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(ElviaSensor(coordinator, description) for description in SENSORS)

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
