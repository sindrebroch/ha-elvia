"""Config flow for Elvia integration."""

from __future__ import annotations

from typing import Any, Dict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ElviaApiClient
from .const import CONF_INTERVAL, CONF_METERING_POINT_ID, DOMAIN, DEFAULT_INTERVAL

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_METERING_POINT_ID): str,
    }
)

class ElviaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Elvia."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            api_key = user_input[CONF_API_KEY]
            metering_point_id = user_input[CONF_METERING_POINT_ID]

            api = ElviaApiClient(
                api_key=api_key,
                metering_point_id=metering_point_id,
                session=async_get_clientsession(self.hass)
            )

            #try:
            #    await api.ping()
            #except Exception:
            #    return self.async_show_form(
            #        step_id="user",
            #        data_schema=SCHEMA,
            #        errors={"base": "cannot_connect"},
            #    )

            return self.async_create_entry(
                title="Elvia",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors={},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ElviaOptionsFlowHandler(config_entry)


class ElviaOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Elvia client options."""

    def __init__(self, config_entry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] or None = None
    ) -> FlowResult:
        """Manage Elvia options."""

        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {vol.Required(CONF_INTERVAL, default=DEFAULT_INTERVAL): int}
                ),
            )

        return self.async_create_entry(title="Options", data=user_input)
