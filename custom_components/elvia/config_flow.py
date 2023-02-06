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
from .const import CONF_METERING_POINT_ID, DOMAIN, CONF_TOKEN

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_METERING_POINT_ID): str,
        vol.Required(CONF_TOKEN): str
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
            token = user_input[CONF_TOKEN]

            api = ElviaApiClient(
                api_key=api_key,
                metering_point_id=metering_point_id,
                token=token,
                session=async_get_clientsession(self.hass),
            )

            try:
                await api.meteringpoint()
            except Exception:
                return self.async_show_form(
                    step_id="user",
                    data_schema=SCHEMA,
                    errors={"base": "cannot_connect"},
                )

            return self.async_create_entry(
                title="Elvia",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors={},
        )
