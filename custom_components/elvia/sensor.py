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

from .const import DOMAIN, LOGGER
from .coordinator import ElviaDataUpdateCoordinator

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="forbruksledd",
        name="Forbruksledd per kWh",
        icon="mdi:currency-usd",
        native_unit_of_measurement="NOK/kWh",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="kapasitetsledd",
        name="Kapasitetsledd per time",
        icon="mdi:currency-usd",
        native_unit_of_measurement="NOK/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="level_info",
        name="Fixed price level",
    ),
    SensorEntityDescription(
        key="fixed_price",
        name="Fixed price monthly",
        native_unit_of_measurement="kr/month",
    ),
)

MAX_HOURS_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="max_hour_aggregate_current_month_1",
        name="Max hour aggregate current month 1",
    ),
    SensorEntityDescription(
        key="max_hour_aggregate_current_month_2",
        name="Max hour aggregate current month 2",
    ),
    SensorEntityDescription(
        key="max_hour_aggregate_current_month_3",
        name="Max hour aggregate current month 3",
    ),
    SensorEntityDescription(
        key="max_hour_average_current_month",
        name="Max hour average current month",
    ),
    SensorEntityDescription(
        key="max_hour_aggregate_previous_month_1",
        name="Max hour aggregate previous month 1",
    ),
    SensorEntityDescription(
        key="max_hour_aggregate_previous_month_2",
        name="Max hour aggregate previous month 2",
    ),
    SensorEntityDescription(
        key="max_hour_aggregate_previous_month_3",
        name="Max hour aggregate previous month 3",
    ),
    SensorEntityDescription(
        key="max_hour_average_previous_month",
        name="Max hour average previous month",
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

    async_add_entities([
        ElviaMaxHourAverageSensor(coordinator, True),
        ElviaMaxHourSensor(coordinator, True, 1),
        ElviaMaxHourSensor(coordinator, True, 2),
        ElviaMaxHourSensor(coordinator, True, 3),
        ElviaMaxHourAverageSensor(coordinator, False),
        ElviaMaxHourSensor(coordinator, False, 1),
        ElviaMaxHourSensor(coordinator, False, 2),
        ElviaMaxHourSensor(coordinator, False, 3),
    ])


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

class ElviaMaxHourCurrentMonthAverageSensor(ElviaSensor):
    """Define a ElviaMaxHourSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.mapped_maxhours['current_month']['average']

class ElviaMaxHourPreviousMonthAverageSensor(ElviaSensor):
    """Define a ElviaMaxHourSensor entity."""

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.mapped_maxhours['previous_month']['average']

class ElviaMaxHourAverageSensor(ElviaSensor):
    """Define a ElviaMaxHourSensor entity."""

    def __init__(
        self,
        coordinator: ElviaDataUpdateCoordinator,
        current_month: bool,
    ) -> None:
        """Initialize."""

        self.month = "current_month" if current_month else "previous_month"
        month_str = "current month" if current_month else "previous month"
        description = SensorEntityDescription(
            key=f"max_hour_average_{self.month}",
            name=f"Average {month_str} max hours",
        )
        super().__init__(coordinator, description, "elvia")

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self.coordinator.mapped_maxhours[self.month]['uom']

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.mapped_maxhours[self.month]['average']

class ElviaMaxHourSensor(ElviaSensor):
    """Define a ElviaMaxHourSensor entity."""

    def __init__(
        self,
        coordinator: ElviaDataUpdateCoordinator,
        current_month: bool,
        sensor_index: int,
    ) -> None:
        """Initialize."""

        self.sensor_index = str(sensor_index)
        self.month = "current_month" if current_month else "previous_month"
        month_str = "Current month" if current_month else "Previous month"
        description = SensorEntityDescription(
            key=f"max_hour_{self.month}_{sensor_index}",
            name=f"{month_str} max hour {sensor_index}",
        )
        super().__init__(coordinator, description, "elvia")

    def update_from_data(self) -> None:
        self.sensor_data = self.coordinator.mapped_maxhours[self.month][self.sensor_index]['value']

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self.coordinator.mapped_maxhours[self.month][self.sensor_index]['uom']

    @property
    def extra_state_attributes(self):
        return {
            "startTime": self.coordinator.mapped_maxhours[self.month][self.sensor_index]['startTime'],
            "endTime": self.coordinator.mapped_maxhours[self.month][self.sensor_index]['endTime']
        }