# custom_components/warema_lamaxa/cover.py

"""Cover platform for Warema Lamaxa custom integration."""
import logging

from homeassistant.components.cover import (
    CoverEntity,
    ATTR_POSITION,
    CoverEntityFeature,
)
from .const import DOMAIN, CMD_ACTION

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Lamaxa cover from config entry."""
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LamaxaCover(coord)], update_before_add=True)


class LamaxaCover(CoverEntity):
    """Cover entity to control a Warema Lamaxa Dach."""

    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.SET_POSITION
    )

    def __init__(self, coord):
        """Initialize."""
        self.coord = coord
        self._attr_name = f"Lamaxa Dach @{coord.host}"
        self._attr_unique_id = f"{coord.dest_id}_lamaxa_cover"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coord.dest_id)},
            "name": f"Lamaxa Dach @{coord.host}",
            "manufacturer": "Warema",
            "model": "Lamaxa",
            "configuration_url": f"http://{coord.host}",
        }

    @property
    def is_closed(self) -> bool:
        """Return True if cover is fully closed."""
        return self.current_cover_position == 0

    @property
    def current_cover_position(self) -> int:
        """Return current position of cover in percent (0 closed, 100 open)."""
        rot = self.coord.data["productData"][0]["value"]["rotation"]
        # Convert from range -45…90 to 0…100
        return round((rot + 45) / 135 * 100)

    async def async_open_cover(self, **kwargs):
        """Open cover to 100%."""
        await self._send_rotation(90)

    async def async_close_cover(self, **kwargs):
        """Close cover to 0%."""
        await self._send_rotation(-45)

    async def async_set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        position = kwargs.get(ATTR_POSITION)
        # Map 0…100% back to rotation -45…90
        rotation = int(-45 + (position / 100) * 135)
        await self._send_rotation(rotation)

    async def _send_rotation(self, rotation: int) -> None:
        """Helper to send a rotation command to the API."""
        payload = {
            "protocolVersion": "1.0",
            "command": CMD_ACTION,
            "source": 2,
            "responseType": 0,
            "actions": [
                {
                    "destinationId": self.coord.dest_id,
                    "actionId": 6,
                    "actiontype": 2,
                    "parameters": {"rotation": rotation},
                }
            ],
        }
        try:
            await self.coord.session.post(
                f"http://{self.coord.host}/commonCommand", json=payload
            )
        except Exception as err:
            _LOGGER.error("Error sending rotation command: %s", err)
