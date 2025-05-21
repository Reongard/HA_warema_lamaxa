"""Config flow for Warema Lamaxa integration."""
import asyncio
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_DEST_ID,
    DEFAULT_TIMEOUT,
    CMD_GET_CONFIG
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA = vol.Schema({
    vol.Required(CONF_HOST, default="192.168.2.156"): str
})

class LamaxaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Warema Lamaxa."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """First step: ask for host and fetch the Lamaxa destination ID."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA
            )

        host = user_input[CONF_HOST]
        session = async_get_clientsession(self.hass)

        # Try to connect and call getConfiguration
        try:
            resp = await session.post(
                f"http://{host}/commonCommand",
                json={
                    "protocolVersion": "1.0",
                    "command": CMD_GET_CONFIG,
                    "source": 2
                },
                timeout=DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            data = await resp.json()
        except (ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Cannot connect to %s: %s", host, err)
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA,
                errors={"base": "cannot_connect"}
            )

        # Pick only the Dach device (names[0] == "L50" or "L70")
        dest_id = None
        for d in data.get("destinations", []):
            if d.get("names", [""])[0] in ("L50", "L70"):
                dest_id = d.get("id")
                break

        if dest_id is None:
            _LOGGER.error("No L50/L70 Lamaxa device found in: %s", data)
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA,
                errors={"base": "no_destination"}
            )

        # Create the config entry
        await self.async_set_unique_id(str(dest_id))
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=f"Warema Lamaxa @ {host}",
            data={
                CONF_HOST: host,
                CONF_DEST_ID: dest_id
            }
        )
