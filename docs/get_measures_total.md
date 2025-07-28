# Get Measures Total

[← Get States](get_states.md) | [Back to Documentation](index.md) | [Next: Switch Control →](switch.md)

Retrieve total measures (power and energy) for a specific device.

## Method

```python
async def get_measures_total(self, auth_token: str, device_id: str) -> list[Measure]
```

## Description

Fetches cumulative measurements for a specific device. This typically includes total power and energy values. Not all devices support total measures - some devices will raise a `MyLightSystemsMeasuresTotalNotSupportedError`.

## Parameters

| Parameter    | Type  | Required | Description                                        |
| ------------ | ----- | -------- | -------------------------------------------------- |
| `auth_token` | `str` | Yes      | Authentication token obtained from [auth](auth.md) |
| `device_id`  | `str` | Yes      | ID of the device to get measures for               |

## Returns

Returns a list of [`Measure`](models.md#measure) objects, each containing:
- `type` (str): Type of measurement (e.g., "power", "energy")
- `value` (float): Measured value
- `unit` (str): Unit of measurement (e.g., "W", "Ws")

## Sample Usage

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient
from mylightsystems.exceptions import MyLightSystemsMeasuresTotalNotSupportedError

async def main():
    async with MyLightSystemsApiClient() as client:
        # First authenticate
        auth = await client.auth("user@example.com", "password")

        # Get devices to find a device ID
        devices = await client.get_devices(auth.token)
        device_id = devices[0].id  # Use first device

        try:
            measures = await client.get_measures_total(auth.token, device_id)
            print(f"Measures for device {device_id}:")

            for measure in measures:
                print(f"- {measure.type}: {measure.value} {measure.unit}")

        except MyLightSystemsMeasuresTotalNotSupportedError:
            print(f"Device {device_id} does not support total measures")
        except MyLightSystemsUnauthorizedError:
            print("Token expired or invalid")

asyncio.run(main())
```

## Sample Response

```json
{
    "status": "ok",
    "measure": {
        "values": [
            {
                "type": "power",
                "value": 97277207.27799994,
                "unit": "W"
            },
            {
                "type": "energy",
                "value": 28583960976.390007,
                "unit": "Ws"
            }
        ]
    }
}
```

The response is automatically parsed into a list of `Measure` objects:

```python
[
    Measure(
        type="power",
        value=97277207.27799994,
        unit="W"
    ),
    Measure(
        type="energy",
        value=28583960976.390007,
        unit="Ws"
    )
]
```

## Measurement Types

Common measurement types include:

### Power
- **Type**: `"power"`
- **Unit**: `"W"` (Watts)
- **Description**: Current power usage/generation

### Energy
- **Type**: `"energy"`
- **Unit**: `"Ws"` (Watt-seconds)
- **Description**: Cumulative energy consumed/produced

## Device Compatibility

Not all devices support total measures. Devices that typically support this endpoint:
- Production counters
- Consumption counters
- Battery devices
- Master devices with aggregated data

Devices that typically don't support this endpoint:
- Simple relay devices
- Ethernet devices without sensors
- Virtual devices

## Exceptions

This method can raise the following exceptions:

### MyLightSystemsMeasuresTotalNotSupportedError
Raised when the specified device doesn't support total measures.

```python
from mylightsystems.exceptions import MyLightSystemsMeasuresTotalNotSupportedError

try:
    measures = await client.get_measures_total(auth.token, device_id)
except MyLightSystemsMeasuresTotalNotSupportedError:
    print(f"Device {device_id} does not support total measures")
```

### MyLightSystemsUnauthorizedError
Raised when the authentication token is invalid or expired.

```python
from mylightsystems.exceptions import MyLightSystemsUnauthorizedError

try:
    measures = await client.get_measures_total(auth.token, device_id)
except MyLightSystemsUnauthorizedError:
    print("Authentication token is invalid or expired")
```

### MyLightSystemsConnectionError
Raised when there's a network connection issue.

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError

try:
    measures = await client.get_measures_total(auth.token, device_id)
except MyLightSystemsConnectionError:
    print("Failed to connect to API")
```
