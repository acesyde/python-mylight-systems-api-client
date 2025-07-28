# Switch Control

[← Get Measures](get_measures_total.md) | [Back to Documentation](index.md) | [Reference: Models →](models.md)

Control the on/off state of switchable devices (relays, outlets, etc.).

## Method

```python
async def switch(self, auth_token: str, device_id: str, value: bool) -> SwitchState
```

## Description

Changes the switch state of a controllable device. This is typically used for relay devices, smart outlets, or other devices that can be turned on/off remotely. Not all devices support switching - some will raise exceptions if switching is not allowed.

## Parameters

| Parameter    | Type   | Required | Description                                        |
| ------------ | ------ | -------- | -------------------------------------------------- |
| `auth_token` | `str`  | Yes      | Authentication token obtained from [auth](auth.md) |
| `device_id`  | `str`  | Yes      | ID of the device to control                        |
| `value`      | `bool` | Yes      | New switch state (`True` = on, `False` = off)      |

## Returns

Returns a [`SwitchState`](models.md#switchstate) object containing:
- `state` (bool): Confirmed new state of the device (True = on, False = off)

## Sample Usage

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient
from mylightsystems.exceptions import (
    MyLightSystemsSwitchNotAllowedError,
    MyLightSystemsUnknownDeviceError
)

async def main():
    async with MyLightSystemsApiClient() as client:
        # First authenticate
        auth = await client.auth("user@example.com", "password")

        # Get devices to find a switchable device
        devices = await client.get_devices(auth.token)

        # Find a relay or switchable device
        switchable_device = None
        for device in devices:
            if device.type in ['sw', 'vrt']:  # Switch or virtual device
                switchable_device = device
                break

        if switchable_device:
            device_id = switchable_device.id

            try:
                # Turn device on
                print(f"Turning on device {device_id}...")
                result = await client.switch(auth.token, device_id, True)
                print(f"Device is now: {'ON' if result.state else 'OFF'}")

                # Wait a moment, then turn it off
                await asyncio.sleep(2)
                print(f"Turning off device {device_id}...")
                result = await client.switch(auth.token, device_id, False)
                print(f"Device is now: {'ON' if result.state else 'OFF'}")

            except MyLightSystemsSwitchNotAllowedError:
                print(f"Device {device_id} does not support switching")
            except MyLightSystemsUnknownDeviceError:
                print(f"Device {device_id} was not found")
            except MyLightSystemsUnauthorizedError:
                print("Token expired or invalid")
        else:
            print("No switchable devices found")

asyncio.run(main())
```

## Sample Response

```json
{
    "status": "ok",
    "state": "on"
}
```

The response is automatically parsed into a `SwitchState` object:

```python
SwitchState(state=True)  # True for "on", False for "off"
```

## Switchable Device Types

### Relay Devices (`sw`)
- Physical relay switches
- Can control connected appliances
- Most common switchable device type
- Examples: Smart outlets, relay modules

## Ethernet devices (`eth`)
- Powerline Ethernet adapters with integrated smart switch
- Provide network connectivity through home electrical wiring
- Allow remote power control of connected devices
- Combine networking and power management functionality
- Examples: Smart powerline adapters, ethernet-enabled smart outlets

## Device Compatibility

**Devices that typically support switching:**
- Relay devices (`type: "sw"`)
- Ethernet devices (`type: "eth"`)

**Devices that typically don't support switching:**
- Some master devices (`type: "mst"`)
- Virtual devices (`type: "vrt"`)
- Counter devices (`type: "cmp"`)
- Composite counter devices (`type: "gmd"`)
- Battery devices (`type: "bat"`)

## State Confirmation

The API returns the actual state after the switch operation. In most cases, this will match the requested state, but there are scenarios where it might differ:

- **Hardware failure**: Device cannot physically switch
- **Safety override**: System prevents switch due to safety conditions
- **Power limitations**: Insufficient power to turn on device
- **Timing issues**: State change in progress but not yet complete

Always check the returned state to confirm the operation succeeded:

```python
# Request to turn on
result = await client.switch(auth.token, device_id, True)
if result.state:
    print("Device successfully turned ON")
else:
    print("Device failed to turn ON or is still OFF")
```

## Exceptions

This method can raise the following exceptions:

### MyLightSystemsSwitchNotAllowedError
Raised when the device doesn't support switching or switching is not allowed for the current device state.

```python
from mylightsystems.exceptions import MyLightSystemsSwitchNotAllowedError

try:
    result = await client.switch(auth.token, device_id, True)
except MyLightSystemsSwitchNotAllowedError:
    print("This device cannot be switched")
```

### MyLightSystemsUnknownDeviceError
Raised when the specified device ID doesn't exist or is not accessible.

```python
from mylightsystems.exceptions import MyLightSystemsUnknownDeviceError

try:
    result = await client.switch(auth.token, "invalid_device_id", True)
except MyLightSystemsUnknownDeviceError:
    print("Device not found")
```

### MyLightSystemsUnauthorizedError
Raised when the authentication token is invalid or expired.

```python
from mylightsystems.exceptions import MyLightSystemsUnauthorizedError

try:
    result = await client.switch("invalid_token", device_id, True)
except MyLightSystemsUnauthorizedError:
    print("Authentication token is invalid or expired")
```

### MyLightSystemsConnectionError
Raised when there's a network connection issue.

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError

try:
    result = await client.switch(auth.token, device_id, True)
except MyLightSystemsConnectionError:
    print("Failed to connect to API")
```

## Best Practices

1. **Check device capabilities**: Use [`get_devices`](get_devices.md) first to identify switchable devices
2. **Handle exceptions**: Always wrap switch calls in try-catch blocks
3. **Verify state**: Check the returned state matches your expectation
4. **Rate limiting**: Don't switch devices too frequently to avoid system stress
5. **State monitoring**: Use [`get_states`](get_states.md) to monitor state changes over time

## See Also

- [Get Devices](get_devices.md) - Identify switchable devices
- [Get Device States](get_states.md) - Monitor switch state changes
- [Data Models: RelayDevice](models.md#relaydevice) - Switchable device type
- [Data Models: SwitchState](models.md#switchstate) - Switch result object
- [Exception: SwitchNotAllowedError](exceptions.md#mylightsystemsswitchnotallowederror) - Switch compatibility info
- [Advanced Usage: Smart Automation](README.md#smart-device-automation) - Intelligent device control example
