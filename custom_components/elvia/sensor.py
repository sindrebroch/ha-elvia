"""Support for Elvia sensors."""

from __future__ import annotations

from typing import Any, cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as ELVIA_DOMAIN
from .coordinator import ElviaDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Elvia sensor."""
    coordinator: ElviaDataUpdateCoordinator = hass.data[ELVIA_DOMAIN][entry.entry_id]

class ElviaSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Elvia sensor."""

    coordinator: ElviaDataUpdateCoordinator
    sensor_data: Any

    def __init__(
        self,
        coordinator: ElviaDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize a Elvia sensor."""

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
        """Update attributes based on new data."""
        self.sensor_data = self.coordinator.data.__getattribute__(self.entity_description.key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        
        self.update_from_data()
        super()._handle_coordinator_update()

