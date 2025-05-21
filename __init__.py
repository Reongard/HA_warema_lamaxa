# custom_components/warema_lamaxa/__init__.py

"""Warema Lamaxa integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
# 1) Direkt importieren statt über hass.helpers
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_HOST, CONF_DEST_ID
from .coordinator import LamaxaCoordinator

_LOGGER = logging.getLogger(__name__)

# 2) Nutze hier eine Liste statt harter Schleife
PLATFORMS = ["cover", "sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration (placeholder)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry (called when the user finishes the UI flow)."""
    host = entry.data[CONF_HOST]
    dest_id = entry.data[CONF_DEST_ID]
    # 3) Direkt auf Session-Funktion zugreifen
    session = async_get_clientsession(hass)

    # 4) Coordinator initialisieren und ersten Refresh abwarten
    coord = LamaxaCoordinator(hass, session, host, dest_id)
    await coord.async_config_entry_first_refresh()

    # 5) Coordinator speichern
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coord

    # 6) Plattformen gemeinsam starten (await statt create_task)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and remove its platforms."""
    # alle Plattformen entladen
    unload_ok = await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, platform)
            for platform in PLATFORMS
        ]
    )
    if all(unload_ok):
        hass.data[DOMAIN].pop(entry.entry_id, None)
        return True
    return False
