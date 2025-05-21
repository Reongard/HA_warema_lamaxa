"""Data coordinator for Warema Lamaxa integration."""
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CMD_GET_STATUS, DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)

class LamaxaCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch status data from Warema Lamaxa."""

    def __init__(self, hass, session, host, dest_id):
        """Initialize the update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="warema_lamaxa",
            update_interval=timedelta(seconds=60)
        )
        self.session = session
        self.host = host
        self.dest_id = dest_id

    async def _async_update_data(self):
        """Fetch data from the Warema API."""
        try:
            resp = await self.session.post(
                f"http://{self.host}/commonCommand",
                json={
                    "protocolVersion": "1.0",
                    "command": CMD_GET_STATUS,
                    "source": 2,
                    "destinations": [self.dest_id]
                },
                timeout=DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            data = await resp.json()
            return data["details"][0]["data"]
        except Exception as err:
            _LOGGER.error("Error fetching status data: %s", err)
            raise UpdateFailed(err)
