"""The Elvia component."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ElviaApiClient
from .const import (
    CONF_INTERVAL,
    CONF_METERING_POINT_ID,
    DEFAULT_INTERVAL,
    DOMAIN as ELVIA_DOMAIN,
    PLATFORMS,
)
from .coordinator import ElviaDataUpdateCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""

    hass.data.setdefault(ELVIA_DOMAIN, {})

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_INTERVAL: entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL),
            },
        )

    api = ElviaApiClient(
        session=async_get_clientsession(hass),
        api_key=entry.data[CONF_API_KEY],
        metering_point_id=entry.data[CONF_METERING_POINT_ID]
    )
    coordinator = ElviaDataUpdateCoordinator(
        hass,
        name="Elvia",
        api=api,
        update_interval=entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[ELVIA_DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):
    """Unload entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[ELVIA_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
