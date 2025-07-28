# Exceptions

[← Data Models](models.md) | [Back to Documentation](index.md)

This document describes all custom exceptions used by the MyLightSystems API Client and how to handle them.

## Exception Hierarchy

```
MyLightSystemsError (base)
├── MyLightSystemsConnectionError
├── MyLightSystemsInvalidAuthError
├── MyLightSystemsUnauthorizedError
├── MyLightSystemsUnknownDeviceError
├── MyLightSystemsMeasuresTotalNotSupportedError
└── MyLightSystemsSwitchNotAllowedError
```

## Table of Contents

- [MyLightSystemsError](#mylightsystemserror) (Base exception)
- [MyLightSystemsConnectionError](#mylightsystemsconnectionerror)
- [MyLightSystemsInvalidAuthError](#mylightsystemsinvalidautherror)
- [MyLightSystemsUnauthorizedError](#mylightsystemsunauthorizederror)
- [MyLightSystemsUnknownDeviceError](#mylightsystemsunknowndeviceerror)
- [MyLightSystemsMeasuresTotalNotSupportedError](#mylightsystemsmeasurestotalnotsupportederror)
- [MyLightSystemsSwitchNotAllowedError](#mylightsystemsswitchnotallowederror)
- [Exception Handling Patterns](#exception-handling-patterns)

---

## MyLightSystemsError

Base exception class for all MyLightSystems API errors.

```python
class MyLightSystemsError(Exception):
    """Generic exception."""
```

### Usage

Use this as a catch-all for any API-related error:

```python
from mylightsystems.exceptions import MyLightSystemsError

try:
    # Any API call
    auth = await client.auth("email", "password")
except MyLightSystemsError as e:
    print(f"API error occurred: {e}")
```

---

## MyLightSystemsConnectionError

Raised when there's a network connection issue.

```python
class MyLightSystemsConnectionError(MyLightSystemsError):
    """Connection error."""
```

### When Raised

- **Timeout**: Request takes longer than `request_timeout` (default: 10 seconds)
- **Network unreachable**: No internet connection or API server down
- **DNS resolution failure**: Cannot resolve API hostname
- **Connection refused**: API server refusing connections
- **SSL/TLS errors**: Certificate or encryption issues

### Affected Methods

All API methods can raise this exception:
- [`auth`](auth.md)
- [`get_profile`](get_profile.md)
- [`get_devices`](get_devices.md)
- [`get_measures_total`](get_measures_total.md)
- [`get_states`](get_states.md)
- [`switch`](switch.md)

### Handling

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError
import asyncio

async def robust_api_call():
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            auth = await client.auth("email", "password")
            return auth
        except MyLightSystemsConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed (attempt {attempt + 1}), retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"All connection attempts failed: {e}")
                raise
```

---

## MyLightSystemsInvalidAuthError

Raised when authentication fails due to invalid credentials.

```python
class MyLightSystemsInvalidAuthError(MyLightSystemsError):
    """Invalid authentication error."""
```

### When Raised

- **Invalid credentials**: Wrong email/password combination
- **Undefined email**: Email parameter is missing or empty
- **Undefined password**: Password parameter is missing or empty

### Affected Methods

- [`auth`](auth.md)

### API Response Triggers

This exception is raised when the API returns:
```json
{
    "status": "error",
    "error": "invalid.credentials"
}
```
```json
{
    "status": "error",
    "error": "undefined.email"
}
```
```json
{
    "status": "error",
    "error": "undefined.password"
}
```

### Handling

```python
from mylightsystems.exceptions import MyLightSystemsInvalidAuthError

try:
    auth = await client.auth("user@example.com", "wrong_password")
except MyLightSystemsInvalidAuthError:
    print("Login failed: Please check your email and password")
    # Prompt user for correct credentials
```

---

## MyLightSystemsUnauthorizedError

Raised when a request is made with an invalid or expired token.

```python
class MyLightSystemsUnauthorizedError(MyLightSystemsError):
    """Unauthorized error."""
```

### When Raised

- **Invalid token**: Authentication token is malformed or fake
- **Expired token**: Token has exceeded its lifetime
- **Revoked token**: Token has been manually revoked
- **Insufficient permissions**: Token lacks required permissions

### Affected Methods

All authenticated methods can raise this exception:
- [`get_profile`](get_profile.md)
- [`get_devices`](get_devices.md)
- [`get_measures_total`](get_measures_total.md)
- [`get_states`](get_states.md)
- [`switch`](switch.md)

### API Response Trigger

This exception is raised when the API returns:
```json
{
    "status": "error",
    "error": "not.authorized"
}
```

### Handling

```python
from mylightsystems.exceptions import (
    MyLightSystemsUnauthorizedError,
    MyLightSystemsInvalidAuthError
)

async def auto_reauth_wrapper(client, email, password, api_call):
    """Automatically re-authenticate if token expires."""
    try:
        return await api_call()
    except MyLightSystemsUnauthorizedError:
        print("Token expired, re-authenticating...")
        try:
            auth = await client.auth(email, password)
            # Update token and retry
            return await api_call()
        except MyLightSystemsInvalidAuthError:
            print("Re-authentication failed")
            raise

# Usage
devices = await auto_reauth_wrapper(
    client, email, password,
    lambda: client.get_devices(auth.token)
)
```

---

## MyLightSystemsUnknownDeviceError

Raised when trying to interact with a device that doesn't exist.

```python
class MyLightSystemsUnknownDeviceError(MyLightSystemsError):
    """Unknown device error."""
```

### When Raised

- **Invalid device ID**: Device ID doesn't exist in the system
- **Device removed**: Device was recently removed but ID still cached
- **Access restricted**: Device exists but not accessible to current user

### Affected Methods

- [`switch`](switch.md)

### API Response Trigger

This exception is raised when the API returns:
```json
{
    "status": "error",
    "error": "device.not.found"
}
```

### Handling

```python
from mylightsystems.exceptions import MyLightSystemsUnknownDeviceError

async def safe_switch(client, auth_token, device_id, state):
    """Safely switch a device with error handling."""
    try:
        result = await client.switch(auth_token, device_id, state)
        return result
    except MyLightSystemsUnknownDeviceError:
        print(f"Device {device_id} not found - refreshing device list...")
        # Refresh device list to get current devices
        devices = await client.get_devices(auth_token)
        available_ids = [d.id for d in devices]
        print(f"Available devices: {available_ids}")
        return None
```

---

## MyLightSystemsMeasuresTotalNotSupportedError

Raised when trying to get total measures from a device that doesn't support them.

```python
class MyLightSystemsMeasuresTotalNotSupportedError(MyLightSystemsError):
    """Device doesn't support measures total error."""
```

### When Raised

- **Incompatible device type**: Device type doesn't support total measures
- **No sensors**: Device has no measurement sensors
- **Configuration issue**: Device sensors not properly configured

### Affected Methods

- [`get_measures_total`](get_measures_total.md)

### API Response Trigger

This exception is raised when the API returns:
```json
{
    "status": "error",
    "error": "device.not.supports.total.measures"
}
```

### Device Compatibility

**Typically supported:**
- Production counters
- Consumption counters
- Battery devices
- Master devices with sensors

**Typically not supported:**
- Simple relay devices
- Ethernet devices without sensors
- Virtual devices
- Some counter devices

### Handling

```python
from mylightsystems.exceptions import MyLightSystemsMeasuresTotalNotSupportedError

async def get_all_available_measures(client, auth_token):
    """Get measures for all compatible devices."""
    devices = await client.get_devices(auth_token)
    measures_data = {}

    for device in devices:
        try:
            measures = await client.get_measures_total(auth_token, device.id)
            measures_data[device.id] = measures
            print(f"✓ {device.name}: {len(measures)} measures")
        except MyLightSystemsMeasuresTotalNotSupportedError:
            print(f"✗ {device.name}: Total measures not supported")

    return measures_data
```

---

## MyLightSystemsSwitchNotAllowedError

Raised when trying to switch a device that doesn't support switching.

```python
class MyLightSystemsSwitchNotAllowedError(MyLightSystemsError):
    """Switch not allowed error."""
```

### When Raised

- **Non-switchable device**: Device type doesn't support switching
- **Safety lockout**: Device locked for safety reasons
- **Hardware failure**: Device cannot physically switch
- **Configuration restriction**: Switching disabled in device settings

### Affected Methods

- [`switch`](switch.md)

### API Response Trigger

This exception is raised when the API returns:
```json
{
    "status": "error",
    "error": "switch.not.allowed"
}
```

### Device Compatibility

**Typically switchable:**
- Relay devices (`type: "sw"`)
- Virtual devices (`type: "vrt"`)
- Some master devices (`type: "mst"`)

**Typically not switchable:**
- Counter devices (`type: "cmp"`)
- Composite counters (`type: "gmd"`)
- Ethernet devices (`type: "eth"`)
- Battery devices (`type: "bat"`)

### Handling

```python
from mylightsystems.exceptions import MyLightSystemsSwitchNotAllowedError

async def identify_switchable_devices(client, auth_token):
    """Find all devices that can be switched."""
    devices = await client.get_devices(auth_token)
    switchable = []

    for device in devices:
        try:
            # Try to get current state (no actual change)
            current_state = hasattr(device, 'state') and device.state
            await client.switch(auth_token, device.id, current_state)
            switchable.append(device)
            print(f"✓ {device.name} is switchable")
        except MyLightSystemsSwitchNotAllowedError:
            print(f"✗ {device.name} is not switchable")

    return switchable
```

---

## Exception Handling Patterns

### Pattern 1: Specific Exception Handling

Handle each exception type specifically:

```python
from mylightsystems.exceptions import *

async def comprehensive_api_call():
    try:
        auth = await client.auth("email", "password")
        devices = await client.get_devices(auth.token)

        for device in devices:
            try:
                if hasattr(device, 'state'):
                    await client.switch(auth.token, device.id, True)
            except MyLightSystemsSwitchNotAllowedError:
                print(f"Cannot switch {device.name}")
            except MyLightSystemsUnknownDeviceError:
                print(f"Device {device.name} not found")

    except MyLightSystemsInvalidAuthError:
        print("Invalid credentials")
    except MyLightSystemsConnectionError:
        print("Connection failed")
    except MyLightSystemsUnauthorizedError:
        print("Authentication expired")
```

### Pattern 2: Hierarchical Exception Handling

Use the base exception for common handling:

```python
from mylightsystems.exceptions import MyLightSystemsError, MyLightSystemsConnectionError

async def robust_operation():
    try:
        # API operations here
        pass
    except MyLightSystemsConnectionError as e:
        # Handle connection issues specifically
        print(f"Connection problem: {e}")
        # Maybe retry logic
    except MyLightSystemsError as e:
        # Handle all other API errors
        print(f"API error: {e}")
        # General error handling
```

### Pattern 3: Retry with Exponential Backoff

For connection errors:

```python
import asyncio
from mylightsystems.exceptions import MyLightSystemsConnectionError

async def retry_with_backoff(operation, max_retries=3, base_delay=1):
    """Retry operation with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await operation()
        except MyLightSystemsConnectionError as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
            await asyncio.sleep(delay)
```

### Pattern 4: Context Manager with Cleanup

```python
from mylightsystems.exceptions import MyLightSystemsError

class MyLightSystemsSession:
    def __init__(self, client, email, password):
        self.client = client
        self.email = email
        self.password = password
        self.auth = None

    async def __aenter__(self):
        try:
            self.auth = await self.client.auth(self.email, self.password)
            return self
        except MyLightSystemsError:
            await self.client.close()
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, MyLightSystemsError):
            print(f"Session ended with error: {exc_val}")
        await self.client.close()

# Usage
async with MyLightSystemsSession(client, "email", "password") as session:
    devices = await client.get_devices(session.auth.token)
```
