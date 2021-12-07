"""Config flow to configure the Elvia integration."""

from typing import Any, Dict

import voluptuous as vol
from voluptuous.schema_builder import Schema

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.const import CONF_API_KEY
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ElviaApiClient
from .const import CONF_INTERVAL, CONF_METERING_POINT_ID, DEFAULT_INTERVAL, DOMAIN as ELVIA_DOMAIN

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_METERING_POINT_ID): str
    }
)


class ElviaFlowHandler(ConfigFlow, domain=ELVIA_DOMAIN):
    """Handle a Elvia config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""

        self.user_input: Dict[str, Any] = {}
        self.title: str = ""

    def show_user_form(self, errors: Dict[str, Any] = {}) -> FlowResult:
        """Show user form."""

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
            last_step=False,
        )

    async def async_step_user(
        self,
        user_input: Dict[str, Any] or None = None,
    ) -> FlowResult:
        """Handle a flow initiated by the user."""

        if user_input is None:
            return self.show_user_form()

        self.user_input = user_input

        api = ElviaApiClient(
            async_get_clientsession(self.hass),
            user_input[CONF_API_KEY],
            user_input[CONF_METERING_POINT_ID]
        )

        try:
            await api.ping() # TODO assert success
        except Exception:
            return self.show_user_form({"base": "cannot_connect"})

        return self.async_create_entry(title="Elvia")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ElviaOptionsFlowHandler(config_entry)


class ElviaOptionsFlowHandler(OptionsFlow):
    """Handle Elvia client options."""

    def __init__(self, config_entry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] or None = None
    ) -> FlowResult:
        """Manage Elvia options."""

        if user_input is not None:
            return self.async_create_entry(title="Options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {vol.Required(CONF_INTERVAL, default=DEFAULT_INTERVAL): int}
            ),
        )
