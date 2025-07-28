# Get Device States

[← Get Devices](get_devices.md) | [Back to Documentation](index.md) | [Next: Get Measures →](get_measures_total.md)

Retrieve the current states and sensor readings for all devices.

## Method

```python
async def get_states(self, auth_token: str) -> list[DeviceState]
```

## Description

Fetches real-time state information for all devices, including their current status (on/off), sensor measurements, and reporting periods. This provides a snapshot of the entire system's current condition.

## Parameters

| Parameter    | Type  | Required | Description                                        |
| ------------ | ----- | -------- | -------------------------------------------------- |
| `auth_token` | `str` | Yes      | Authentication token obtained from [auth](auth.md) |

## Returns

Returns a list of [`DeviceState`](models.md#devicestate) objects, each containing:
- `device_id` (str): Device identifier
- `report_period` (int): Effective reporting period in seconds
- `state` (bool): Current device state (True = on, False = off)
- `sensor_states` (list): List of [`SensorState`](models.md#sensorstate) objects with sensor readings

## Sample Usage

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient

async def main():
    async with MyLightSystemsApiClient() as client:
        # First authenticate
        auth = await client.auth("user@example.com", "password")

        # Get device states
        try:
            states = await client.get_states(auth.token)
            print(f"Found states for {len(states)} devices:")

            for state in states:
                print(f"Device {state.device_id}:")
                print(f"  State: {'ON' if state.state else 'OFF'}")
                print(f"  Report Period: {state.report_period}s")
                print(f"  Sensors:")

                for sensor in state.sensor_states:
                    measure = sensor.measure
                    type_info = f" ({measure.type})" if measure.type else ""
                    unit_info = f" {measure.unit}" if measure.unit else ""
                    print(f"    {sensor.sensor_id}: {measure.value}{unit_info}{type_info}")
                    print(f"      Last update: {measure.date}")
                print()

        except MyLightSystemsUnauthorizedError:
            print("Token expired or invalid")

asyncio.run(main())
```

## Sample Response

```json
{
    "status": "ok",
    "deviceStates": [
        {
            "deviceId": "F7DFE301A82C",
            "effectiveReportPeriod": 150,
            "state": "off",
            "sensorStates": [
                {
                    "sensorId": "F7DFE301A82C-pow",
                    "measure": {
                        "value": 0.0,
                        "type": "electric_power",
                        "unit": "watt",
                        "date": "2024-07-28 18:03:14"
                    }
                }
            ]
        },
        {
            "deviceId": "xRqpTvwC2GAO9gwo",
            "effectiveReportPeriod": 150,
            "state": "on",
            "sensorStates": [
                {
                    "sensorId": "xRqpTvwC2GAO9gwo-pow",
                    "measure": {
                        "value": -137.46,
                        "type": "electric_power",
                        "unit": "watt",
                        "date": "2024-07-28 18:03:14"
                    }
                }
            ]
        }
    ]
}
```

The response is automatically parsed into `DeviceState` objects:

```python
[
    DeviceState(
        device_id="F7DFE301A82C",
        report_period=150,
        state=False,
        sensor_states=[
            SensorState(
                sensor_id="F7DFE301A82C-pow",
                measure=SensorMeasure(
                    value=0.0,
                    type="electric_power",
                    unit="watt",
                    date=datetime(2024, 7, 28, 18, 3, 14)
                )
            )
        ]
    ),
    DeviceState(
        device_id="xRqpTvwC2GAO9gwo",
        report_period=150,
        state=True,
        sensor_states=[
            SensorState(
                sensor_id="xRqpTvwC2GAO9gwo-pow",
                measure=SensorMeasure(
                    value=-137.46,
                    type="electric_power",
                    unit="watt",
                    date=datetime(2024, 7, 28, 18, 3, 14)
                )
            )
        ]
    )
]
```

## Understanding Sensor Data

### Sensor IDs
Sensors are typically named with the device ID followed by a sensor type:
- `{device_id}-pow`: Power measurement sensor
- `{device_id}-pow_1`, `{device_id}-pow_2`, `{device_id}-pow_3`: Multi-phase power sensors
- `{device_id}-produced_energy`: Energy production sensor
- `{device_id}-soc`: State of charge (battery)

### Measurement Types
Common sensor measurement types:

#### Electric Power
- **Type**: `"electric_power"`
- **Unit**: `"watt"`
- **Description**: Current power consumption/production
- **Note**: Negative values typically indicate power generation

#### Energy Measurements
- **Types**: `"produced_energy"`, `"total_energy"`, `"green_energy"`, `"grid_energy"`
- **Unit**: `"Ws"` (Watt-seconds)
- **Description**: Cumulative energy values

#### Battery Measurements
- **Type**: `"soc"` (State of Charge)
- **Unit**: `"Ws"`
- **Description**: Current battery charge level
- **Type**: `"charge_energy"`, `"discharge_energy"`
- **Description**: Energy charged/discharged from battery

#### Performance Metrics
- **Type**: `"autonomy_rate"`, `"selfconso"`
- **Unit**: Usually percentage (no unit specified)
- **Description**: System performance indicators

### Power Values Interpretation
- **Positive values**: Power consumption (drawing from grid/battery)
- **Negative values**: Power production (feeding into grid/charging battery)
- **Zero values**: No power flow or device is off

## Report Periods

The `report_period` indicates how frequently the device reports data:
- Common values: 150s, 300s (2.5 or 5 minutes)
- Shorter periods = more frequent updates but higher data usage
- Can vary per device based on configuration

## Exceptions

This method can raise the following exceptions:

### MyLightSystemsUnauthorizedError
Raised when the authentication token is invalid or expired.

```python
from mylightsystems.exceptions import MyLightSystemsUnauthorizedError

try:
    states = await client.get_states("invalid_token")
except MyLightSystemsUnauthorizedError:
    print("Authentication token is invalid or expired")
```

### MyLightSystemsConnectionError
Raised when there's a network connection issue.

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError

try:
    states = await client.get_states(auth.token)
except MyLightSystemsConnectionError:
    print("Failed to connect to API")

## See Also

- [Get Devices](get_devices.md) - Get device information first
- [Get Measures Total](get_measures_total.md) - Get cumulative energy data
- [Switch Control](switch.md) - Control device states
- [Data Models: DeviceState](models.md#devicestate) - DeviceState object reference
- [Data Models: SensorState](models.md#sensorstate) - SensorState object reference
- [Advanced Usage: Energy Dashboard](README.md#energy-monitoring-dashboard) - Real-world example
```
