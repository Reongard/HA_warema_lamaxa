from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        LamaxaRotationSensor(coord),
        LamaxaPercentSensor(coord)
    ], update_before_add=True)

class LamaxaRotationSensor(Entity):
    def __init__(self, coord):
        self.coord = coord
        self._attr_name = "Lamaxa Rotation"
        self._attr_unique_id = f"{coord.dest_id}_lamaxa_rotation"
        self._attr_unit_of_measurement = "°"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coord.dest_id)},
            "name": f"Lamaxa Dach @{coord.host}"
        }

    @property
    def state(self):
        return self.coord.data["productData"][0]["value"]["rotation"]

    @property
    def available(self):
        return bool(self.coord.data)

class LamaxaPercentSensor(LamaxaRotationSensor):
    def __init__(self, coord):
        super().__init__(coord)
        self._attr_name = "Lamaxa Öffnungsgrad"
        self._attr_unique_id = f"{coord.dest_id}_lamaxa_percent"
        self._attr_unit_of_measurement = "%"

    @property
    def state(self):
        rot = super().state
        return round((rot + 45) / 135 * 100, 1)
