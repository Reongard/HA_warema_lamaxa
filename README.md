# Warema Lamaxa Custom Integration



Control your Warema Lamaxa roof (models L50 & L70) directly from Home Assistant with this custom integration.

## Features

* Automatically fetches `destinationId` via the Warema WebControl API
* **Cover** entity with Open, Close, and Set Position (0 – 100 %) support
* Two **sensors**:

  * `sensor.lamaxa_rotation` — Roof rotation in degrees (–45 … 90)
  * `sensor.lamaxa_percent` — Roof opening degree in percent (0 … 100)
* Service `warema_lamaxa.set_position` to set position by **rotation** or **percent**
* Localization: German (`de.json`); English is the default fallback

## To-Do

*Add LED control

## Installation


### Manual

1. Create the folder `<config>/custom_components/warema_lamaxa/`
2. Copy these files into that folder:

   * `__init__.py`
   * `manifest.json`
   * `const.py`
   * `config_flow.py`
   * `coordinator.py`
   * `cover.py`
   * `sensor.py`
   * `services.yaml`
   * `translations/de.json` (and optional `en.json`)
   * `logo.png` (for HACS display)
3. Remove any `__pycache__` folder if present.
4. Restart Home Assistant.

## Setup

After restarting, navigate to **Settings → Devices & Services → Add Integration → Warema Lamaxa**. Enter the local IP address of your Warema WebControl device. The integration will automatically retrieve the correct `destinationId`.

## Entities

| Entity ID                        | Type   | Description                    |
| -------------------------------- | ------ | ------------------------------ |
| `cover.lamaxa_dach_lamaxa_cover` | Cover  | Lamaxa roof (0–100 % slider)   |
| `sensor.lamaxa_rotation`         | Sensor | Roof rotation in degrees (°)   |
| `sensor.lamaxa_percent`          | Sensor | Roof opening degree in percent |

## Services

### `warema_lamaxa.set_position`

Set the roof position via rotation or percent.

| Field      | Type    | Description                    |
| ---------- | ------- | ------------------------------ |
| `rotation` | integer | Rotation in degrees (–45 … 90) |
| `percent`  | integer | Opening percent (0 … 100)      |

**Example:**

```yaml
service: warema_lamaxa.set_position
data:
  percent: 50
```

## Lovelace Examples

### Cover Card

```yaml
type: cover
entity: cover.lamaxa_dach_lamaxa_cover
name: Lamaxa Roof
```

### Preset Buttons

```yaml
type: horizontal-stack
cards:
  - type: button
    name: Closed
    icon: mdi:window-closed
    tap_action:
      action: call-service
      service: warema_lamaxa.set_position
      service_data:
        rotation: -45

  - type: button
    name: One Third
    icon: mdi:window-open-variant
    tap_action:
      action: call-service
      service: warema_lamaxa.set_position
      service_data:
        rotation: 0

  - type: button
    name: Two Thirds
    icon: mdi:window-open
    tap_action:
      action: call-service
      service: warema_lamaxa.set_position
      service_data:
        rotation: 45

  - type: button
    name: Fully Open
    icon: mdi:window-maximize
    tap_action:
      action: call-service
      service: warema_lamaxa.set_position
      service_data:
        rotation: 90
```

## Localization

* German translations can be found in `translations/de.json`.
* English texts are used as a default fallback and do not require an `en.json` file.

## Contributing

Feel free to open issues or submit pull requests in the GitHub repository:

`https://github.com/Reongard/HA_warema_lamaxa`

---

© 2025 Reongard — MIT License
