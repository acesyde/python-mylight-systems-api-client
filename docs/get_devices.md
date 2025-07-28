# Get Devices

[← Get Profile](get_profile.md) | [Back to Documentation](index.md) | [Next: Get States →](get_states.md)

Retrieve a list of all devices connected to the user's MyLightSystems installation.

## Method

```python
async def get_devices(self, auth_token: str) -> list[Device]
```

## Description

Fetches all devices associated with the authenticated user's account. Devices are automatically categorized into different types (master, battery, relay, counter, etc.) based on their characteristics.

## Parameters

| Parameter    | Type  | Required | Description                                        |
| ------------ | ----- | -------- | -------------------------------------------------- |
| `auth_token` | `str` | Yes      | Authentication token obtained from [auth](auth.md) |

## Returns

Returns a list of [`Device`](models.md#device) objects. Each device can be one of several subtypes:
- [`MasterDevice`](models.md#masterdevice) - Main control unit
- [`BatteryDevice`](models.md#batterydevice) - Battery storage
- [`RelayDevice`](models.md#relaydevice) - Switch/relay control
- [`CounterDevice`](models.md#counterdevice) - Energy meter/counter
- [`CompositeCounterDevice`](models.md#compositecounterdevice) - Multi-phase counter
- [`VirtualDevice`](models.md#virtualdevice) - Virtual/software device
- [`EthernetDevice`](models.md#ethernetdevice) - Ethernet-connected device

## Sample Usage

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient
from mylightsystems.models import MasterDevice, BatteryDevice, RelayDevice

async def main():
    async with MyLightSystemsApiClient() as client:
        # First authenticate
        auth = await client.auth("user@example.com", "password")

        # Get devices
        try:
            devices = await client.get_devices(auth.token)
            print(f"Found {len(devices)} devices:")

            for device in devices:
                print(f"- {device.name} ({device.device_type_name})")
                print(f"  ID: {device.id}")
                print(f"  Type: {device.type}")

                # Check device-specific properties
                if isinstance(device, MasterDevice):
                    print(f"  Report Period: {device.report_period}s")
                elif isinstance(device, BatteryDevice):
                    print(f"  Capacity: {device.capacity}%")
                elif isinstance(device, RelayDevice):
                    print(f"  Master: {device.master_id}")

                print(f"  State: {'ON' if hasattr(device, 'state') and device.state else 'OFF'}")
                print()

        except MyLightSystemsUnauthorizedError:
            print("Token expired or invalid")

asyncio.run(main())
```

## Sample Response

```json
{
    "status": "ok",
    "devices": [
        {
            "id": "F8DFE101A81C",
            "name": "Master",
            "type": "mst",
            "serialNumber": "M2202G302058P",
            "reportPeriod": 300,
            "state": "on",
            "deviceTypeId": "asoka_red_plug",
            "typeOverride": "MST-G3",
            "deviceTypeName": "Appareil rouge"
        },
        {
            "id": "E9BC5FA11C75E",
            "name": "Battery 1",
            "type": "bat",
            "batteryCapacity": 100.0,
            "state": "on",
            "deviceTypeId": "my_smart_battery",
            "typeOverride": "MySmartBattery",
            "deviceTypeName": "My Smart Battery"
        },
        {
            "id": "4D9F3281C75E",
            "name": "Relais",
            "type": "sw",
            "state": "off",
            "masterMac": "F8DFE101A81C",
            "masterType": "mst",
            "deviceTypeId": "other_device_type",
            "deviceTypeName": "Autre"
        }
    ]
}
```

The response is automatically parsed into appropriate `Device` subtype objects:

```python
[
    MasterDevice(
        id="F8DFE101A81C",
        name="Master",
        device_type_name="Appareil rouge",
        type="mst",
        type_id="asoka_red_plug",
        state=True,
        report_period=300
    ),
    BatteryDevice(
        id="E9BC5FA11C75E",
        name="Battery 1",
        device_type_name="My Smart Battery",
        type="bat",
        type_id="my_smart_battery",
        state=True,
        capacity=100
    ),
    RelayDevice(
        id="4D9F3281C75E",
        name="Relais",
        device_type_name="Autre",
        type="sw",
        type_id="other_device_type",
        state=False,
        master_id="F8DFE101A81C",
        master_type="mst"
    )
]
```

## Device Types

The API returns different device types with specific properties:

### Master Device (`mst`)
- Controls other devices
- Has `report_period` setting
- Usually one per installation

### Battery Device (`bat`)
- Energy storage system
- Has `capacity` (0-100%)
- Can be charged/discharged

### Relay Device (`sw`)
- Controllable switch/relay
- Has `master_id` and `master_type`
- Can be turned on/off

### Counter Device (`cmp`)
- Energy measurement device
- Has `phase` information
- Tracks consumption/production

### Composite Counter Device (`gmd`)
- Multi-phase energy meter
- Has multiple `children` counters
- Aggregates measurements

### Virtual Device (`vrt`)
- Software-defined device
- Used for calculations/logic
- No physical hardware

### Ethernet Device (`eth`)
- Network-connected device
- Has `master_id` and `master_type`
- Controlled via Ethernet

## Exceptions

This method can raise the following exceptions:

### MyLightSystemsUnauthorizedError
Raised when the authentication token is invalid or expired.

```python
from mylightsystems.exceptions import MyLightSystemsUnauthorizedError

try:
    devices = await client.get_devices("invalid_token")
except MyLightSystemsUnauthorizedError:
    print("Authentication token is invalid or expired")
```

### MyLightSystemsConnectionError
Raised when there's a network connection issue.

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError

try:
    devices = await client.get_devices(auth.token)
except MyLightSystemsConnectionError:
    print("Failed to connect to API")
```
