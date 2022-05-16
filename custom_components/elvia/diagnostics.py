"""Diagnostics support for Elvia."""

from __future__ import annotations

import json
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.elvia.const import DOMAIN
from custom_components.elvia.coordinator import ElviaDataUpdateCoordinator
from custom_components.elvia.models import GridTariffCollection


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    diagnostics: dict[str, Any] = {}

    coordinator: ElviaDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    data: GridTariffCollection = coordinator.data

    diagnostics["tariffPrice"] = json.dumps(data.gridTariff.tariffPrice, default=str)
    diagnostics["tariffType"] = json.dumps(data.gridTariff.tariffType, default=str)

    diagnostics["meteringPointsAndPriceLevels"] = json.dumps(data.meteringPointsAndPriceLevels, default=str)

    return diagnostics