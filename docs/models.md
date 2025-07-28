# Data Models

[← Switch Control](switch.md) | [Back to Documentation](index.md) | [Next: Exceptions →](exceptions.md)

This document describes all data models used by the MyLightSystems API Client.

## Table of Contents

- [Data Models](#data-models)
  - [Table of Contents](#table-of-contents)
  - [Auth](#auth)
    - [Fields](#fields)
    - [Usage](#usage)
  - [Profile](#profile)
    - [Fields](#fields-1)
    - [Usage](#usage-1)
  - [Device Models](#device-models)
    - [Device](#device)
      - [Fields](#fields-2)
    - [BatteryDevice](#batterydevice)
      - [Additional Fields](#additional-fields)
      - [Usage](#usage-2)
    - [RelayDevice](#relaydevice)
      - [Additional Fields](#additional-fields-1)
      - [Usage](#usage-3)
    - [CounterDevice](#counterdevice)
      - [Additional Fields](#additional-fields-2)
    - [CompositeCounterDevice](#compositecounterdevice)
      - [Additional Fields](#additional-fields-3)
    - [VirtualDevice](#virtualdevice)
      - [Additional Fields](#additional-fields-4)
    - [EthernetDevice](#ethernetdevice)
      - [Additional Fields](#additional-fields-5)
    - [MasterDevice](#masterdevice)
      - [Additional Fields](#additional-fields-6)
  - [Measurement Models](#measurement-models)
    - [Measure](#measure)
      - [Fields](#fields-3)
      - [Usage](#usage-4)
    - [SensorMeasure](#sensormeasure)
      - [Fields](#fields-4)
      - [Usage](#usage-5)
  - [State Models](#state-models)
    - [SensorState](#sensorstate)
      - [Fields](#fields-5)
    - [DeviceState](#devicestate)
      - [Fields](#fields-6)
      - [Usage](#usage-6)
    - [SwitchState](#switchstate)
      - [Fields](#fields-7)
      - [Usage](#usage-7)
  - [Type Annotations](#type-annotations)
    - [Example with Type Checking](#example-with-type-checking)

---

## Auth

Authentication token container.

```python
@dataclass
class Auth:
    token: str
```

### Fields

| Field   | Type  | Description                           |
| ------- | ----- | ------------------------------------- |
| `token` | `str` | Authentication token for API requests |

### Usage

Returned by the [`auth`](auth.md) method and used in all subsequent API calls.

```python
auth = await client.auth("email", "password")
profile = await client.get_profile(auth.token)
```

---

## Profile

User profile information.

```python
@dataclass
class Profile:
    id: int
    grid_type: str
    tenant: str
    city: str
    country: str
    postal_code: str
    address: str
```

### Fields

| Field         | Type  | Description                                                |
| ------------- | ----- | ---------------------------------------------------------- |
| `id`          | `int` | Unique user identifier                                     |
| `grid_type`   | `str` | Electrical grid configuration (e.g., "1 phase", "3 phase") |
| `tenant`      | `str` | Tenant/organization identifier                             |
| `city`        | `str` | User's city                                                |
| `country`     | `str` | User's country (ISO country code)                          |
| `postal_code` | `str` | Postal/ZIP code                                            |
| `address`     | `str` | Street address                                             |

### Usage

Returned by the [`get_profile`](get_profile.md) method.

```python
profile = await client.get_profile(auth.token)
print(f"User in {profile.city}, {profile.country}")
```

---

## Device Models

All device types inherit from the base `Device` class and add specific properties.

### Device

Base device class with common properties.

```python
@dataclass
class Device:
    id: str
    name: str
    device_type_name: str
    type: str
    type_id: str
```

#### Fields

| Field              | Type  | Description                                       |
| ------------------ | ----- | ------------------------------------------------- |
| `id`               | `str` | Unique device identifier (MAC address or similar) |
| `name`             | `str` | Human-readable device name                        |
| `device_type_name` | `str` | Localized device type description                 |
| `type`             | `str` | Device type code (e.g., "mst", "bat", "sw")       |
| `type_id`          | `str` | Device type identifier                            |

---

### BatteryDevice

Battery storage device.

```python
@dataclass
class BatteryDevice(Device):
    state: bool
    capacity: int
```

#### Additional Fields

| Field      | Type   | Description                           |
| ---------- | ------ | ------------------------------------- |
| `state`    | `bool` | Current battery state (True = active) |
| `capacity` | `int`  | Battery capacity percentage (0-100)   |

#### Usage

```python
devices = await client.get_devices(auth.token)
for device in devices:
    if isinstance(device, BatteryDevice):
        print(f"Battery {device.name}: {device.capacity}%")
```

---

### RelayDevice

Switchable relay/outlet device.

```python
@dataclass
class RelayDevice(Device):
    state: bool
    master_id: str
    master_type: str
```

#### Additional Fields

| Field         | Type   | Description                                  |
| ------------- | ------ | -------------------------------------------- |
| `state`       | `bool` | Current relay state (True = on, False = off) |
| `master_id`   | `str`  | ID of the controlling master device          |
| `master_type` | `str`  | Type of the master device                    |

#### Usage

```python
# Control a relay device
for device in devices:
    if isinstance(device, RelayDevice):
        await client.switch(auth.token, device.id, True)  # Turn on
```

---

### CounterDevice

Energy measurement device (single phase).

```python
@dataclass
class CounterDevice(Device):
    state: bool
    phase: int
    master_id: str
    master_type: str
```

#### Additional Fields

| Field         | Type   | Description                           |
| ------------- | ------ | ------------------------------------- |
| `state`       | `bool` | Current counter state (True = active) |
| `phase`       | `int`  | Electrical phase number (1, 2, or 3)  |
| `master_id`   | `str`  | ID of the controlling master device   |
| `master_type` | `str`  | Type of the master device             |

---

### CompositeCounterDevice

Multi-phase energy measurement device.

```python
@dataclass
class CompositeCounterDevice(Device):
    master_id: str
    master_type: str
    children: dict[str, int]
```

#### Additional Fields

| Field         | Type             | Description                                |
| ------------- | ---------------- | ------------------------------------------ |
| `master_id`   | `str`            | ID of the controlling master device        |
| `master_type` | `str`            | Type of the master device                  |
| `children`    | `dict[str, int]` | Child devices mapping (device_id -> phase) |

---

### VirtualDevice

Software-defined device.

```python
@dataclass
class VirtualDevice(Device):
    state: bool
```

#### Additional Fields

| Field   | Type   | Description                  |
| ------- | ------ | ---------------------------- |
| `state` | `bool` | Current virtual device state |

---

### EthernetDevice

Ethernet-connected device.

```python
@dataclass
class EthernetDevice(Device):
    master_id: str
    master_type: str
```

#### Additional Fields

| Field         | Type  | Description                         |
| ------------- | ----- | ----------------------------------- |
| `master_id`   | `str` | ID of the controlling master device |
| `master_type` | `str` | Type of the master device           |

---

### MasterDevice

Main control unit device.

```python
@dataclass
class MasterDevice(Device):
    state: bool
    report_period: int
```

#### Additional Fields

| Field           | Type   | Description                        |
| --------------- | ------ | ---------------------------------- |
| `state`         | `bool` | Current master device state        |
| `report_period` | `int`  | Data reporting interval in seconds |

---

## Measurement Models

### Measure

Static measurement value with type and unit.

```python
@dataclass
class Measure:
    type: str
    value: float
    unit: str
```

#### Fields

| Field   | Type    | Description                                |
| ------- | ------- | ------------------------------------------ |
| `type`  | `str`   | Measurement type (e.g., "power", "energy") |
| `value` | `float` | Measured value                             |
| `unit`  | `str`   | Unit of measurement (e.g., "W", "Ws")      |

#### Usage

Returned by [`get_measures_total`](get_measures_total.md).

```python
measures = await client.get_measures_total(auth.token, device_id)
for measure in measures:
    print(f"{measure.type}: {measure.value} {measure.unit}")
```

---

### SensorMeasure

Time-stamped sensor measurement.

```python
@dataclass
class SensorMeasure:
    type: str | None
    value: float
    unit: str | None
    date: datetime
```

#### Fields

| Field   | Type          | Description                    |
| ------- | ------------- | ------------------------------ |
| `type`  | `str \| None` | Measurement type (optional)    |
| `value` | `float`       | Measured value                 |
| `unit`  | `str \| None` | Unit of measurement (optional) |
| `date`  | `datetime`    | Timestamp of the measurement   |

#### Usage

Used within `SensorState` objects from [`get_states`](get_states.md).

---

## State Models

### SensorState

Current state of a single sensor.

```python
@dataclass
class SensorState:
    sensor_id: str
    measure: SensorMeasure
```

#### Fields

| Field       | Type            | Description                |
| ----------- | --------------- | -------------------------- |
| `sensor_id` | `str`           | Unique sensor identifier   |
| `measure`   | `SensorMeasure` | Current sensor measurement |

---

### DeviceState

Current state of a device including all sensors.

```python
@dataclass
class DeviceState:
    device_id: str
    report_period: int
    state: bool
    sensor_states: list[SensorState]
```

#### Fields

| Field           | Type                | Description                           |
| --------------- | ------------------- | ------------------------------------- |
| `device_id`     | `str`               | Device identifier                     |
| `report_period` | `int`               | Effective reporting period in seconds |
| `state`         | `bool`              | Device state (True = on, False = off) |
| `sensor_states` | `list[SensorState]` | List of sensor readings               |

#### Usage

Returned by [`get_states`](get_states.md).

```python
states = await client.get_states(auth.token)
for state in states:
    print(f"Device {state.device_id} is {'ON' if state.state else 'OFF'}")
    for sensor in state.sensor_states:
        print(f"  {sensor.sensor_id}: {sensor.measure.value}")
```

---

### SwitchState

Result of a switch operation.

```python
@dataclass
class SwitchState:
    state: bool
```

#### Fields

| Field   | Type   | Description                                   |
| ------- | ------ | --------------------------------------------- |
| `state` | `bool` | Confirmed device state after switch operation |

#### Usage

Returned by [`switch`](switch.md).

```python
result = await client.switch(auth.token, device_id, True)
if result.state:
    print("Device successfully turned ON")
```

---

## Type Annotations

All models use Python type annotations and are compatible with:
- Type checkers (mypy, pyright)
- IDEs with Python support
- Runtime type checking libraries

### Example with Type Checking

```python
from mylightsystems.models import Device, BatteryDevice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    devices: list[Device] = await client.get_devices(auth.token)

    # Type narrowing
    battery: BatteryDevice
    for device in devices:
        if isinstance(device, BatteryDevice):
            battery = device
            print(f"Battery capacity: {battery.capacity}%")  # Type-safe
```
