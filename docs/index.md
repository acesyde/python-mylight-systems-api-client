# MyLightSystems API Client Documentation

Welcome to the comprehensive documentation for the MyLightSystems Python API Client. This async library provides full access to the MyLight Systems API for monitoring and controlling solar energy systems, home automation devices, and energy management.

## 🚀 Quick Navigation

| Section                             | Description                      |
| ----------------------------------- | -------------------------------- |
| [📋 API Reference](#api-reference)   | Detailed endpoint documentation  |
| [🏗️ Data Models](#data-models)       | All data structures and types    |
| [⚠️ Error Handling](#error-handling) | Exception types and patterns     |
| [🔧 Advanced Usage](#advanced-usage) | Real-world examples and patterns |

---

## 🏃‍♂️ Quick Start

Get up and running in minutes with this complete example:

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient
from mylightsystems.exceptions import MyLightSystemsError

async def main():
    async with MyLightSystemsApiClient() as client:
        try:
            # 1. Authenticate
            auth = await client.auth("your_email@example.com", "your_password")
            print("✅ Authentication successful")

            # 2. Get user profile
            profile = await client.get_profile(auth.token)
            print(f"👤 User: {profile.id} in {profile.city}, {profile.country}")

            # 3. List all devices
            devices = await client.get_devices(auth.token)
            print(f"🏠 Found {len(devices)} devices:")
            for device in devices:
                print(f"   • {device.name} ({device.device_type_name})")

            # 4. Get real-time states
            states = await client.get_states(auth.token)
            print(f"⚡ Device states:")
            for state in states:
                status = "🟢 ON" if state.state else "🔴 OFF"
                print(f"   • Device {state.device_id}: {status}")

        except MyLightSystemsError as e:
            print(f"❌ API Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Installation & Configuration

### Installation

```bash
# Install from PyPI
pip install mylightsystems

# Or from source
pip install git+https://github.com/acesyde/python-mylight-systems-api-client.git
```

### Configuration Options

```python
from mylightsystems.client import MyLightSystemsApiClient

# Basic usage
client = MyLightSystemsApiClient()

# Custom configuration
client = MyLightSystemsApiClient(
    base_url="https://api.mylight-systems.com",  # Custom API endpoint
    request_timeout=30,                          # Timeout in seconds (default: 10)
    session=your_aiohttp_session                 # Optional: custom session
)
```

---

## 📋 API Reference

Complete documentation for all API endpoints:

### Authentication
| Endpoint                | Description                   | Documentation           |
| ----------------------- | ----------------------------- | ----------------------- |
| `auth(email, password)` | Login and obtain access token | [📖 Auth Guide](auth.md) |

### Data Retrieval
| Endpoint                               | Description                   | Documentation                             |
| -------------------------------------- | ----------------------------- | ----------------------------------------- |
| `get_profile(token)`                   | Get user account information  | [📖 Profile Guide](get_profile.md)         |
| `get_devices(token)`                   | List all connected devices    | [📖 Devices Guide](get_devices.md)         |
| `get_states(token)`                    | Get real-time device states   | [📖 States Guide](get_states.md)           |
| `get_measures_total(token, device_id)` | Get total energy measurements | [📖 Measures Guide](get_measures_total.md) |

### Device Control
| Endpoint                          | Description                 | Documentation               |
| --------------------------------- | --------------------------- | --------------------------- |
| `switch(token, device_id, state)` | Control device on/off state | [📖 Switch Guide](switch.md) |

---

## 🏗️ Data Models

Understanding the data structures returned by the API:

### Core Models
- **[`Auth`](models.md#auth)** - Authentication token container
- **[`Profile`](models.md#profile)** - User account information
- **[`DeviceState`](models.md#devicestate)** - Real-time device status
- **[`SwitchState`](models.md#switchstate)** - Switch operation result

### Device Types
- **[`MasterDevice`](models.md#masterdevice)** - Main control unit (type: `mst`)
- **[`BatteryDevice`](models.md#batterydevice)** - Energy storage (type: `bat`)
- **[`RelayDevice`](models.md#relaydevice)** - Controllable switches (type: `sw`)
- **[`CounterDevice`](models.md#counterdevice)** - Energy meters (type: `cmp`)
- **[`CompositeCounterDevice`](models.md#compositecounterdevice)** - Multi-phase meters (type: `gmd`)
- **[`VirtualDevice`](models.md#virtualdevice)** - Software devices (type: `vrt`)
- **[`EthernetDevice`](models.md#ethernetdevice)** - Network devices (type: `eth`)

### Measurement Models
- **[`Measure`](models.md#measure)** - Static measurement values
- **[`SensorMeasure`](models.md#sensormeasure)** - Time-stamped sensor data
- **[`SensorState`](models.md#sensorstate)** - Current sensor readings

📚 **[Complete Models Reference](models.md)** - Detailed field descriptions and usage examples

---

## ⚠️ Error Handling

The client provides comprehensive error handling with specific exception types:

### Exception Hierarchy

```python
MyLightSystemsError (base)
├── MyLightSystemsConnectionError          # Network issues
├── MyLightSystemsInvalidAuthError         # Authentication failures
├── MyLightSystemsUnauthorizedError        # Token expired/invalid
├── MyLightSystemsUnknownDeviceError       # Device not found
├── MyLightSystemsMeasuresTotalNotSupportedError  # Unsupported device
└── MyLightSystemsSwitchNotAllowedError    # Switch not permitted
```

### Error Handling Patterns

```python
from mylightsystems.exceptions import (
    MyLightSystemsConnectionError,
    MyLightSystemsInvalidAuthError,
    MyLightSystemsUnauthorizedError,
    MyLightSystemsError
)

async def robust_api_call():
    try:
        async with MyLightSystemsApiClient() as client:
            auth = await client.auth("email", "password")
            devices = await client.get_devices(auth.token)

    except MyLightSystemsInvalidAuthError:
        print("❌ Invalid credentials - check email/password")
    except MyLightSystemsConnectionError as e:
        print(f"🌐 Connection failed: {e}")
        # Implement retry logic here
    except MyLightSystemsUnauthorizedError:
        print("🔑 Token expired - need to re-authenticate")
    except MyLightSystemsError as e:
        print(f"⚠️ API error: {e}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
```

📚 **[Complete Exception Guide](exceptions.md)** - All exception types with handling patterns

---

## 🔧 Advanced Usage

### Energy Monitoring Dashboard

```python
import asyncio
from datetime import datetime
from mylightsystems.client import MyLightSystemsApiClient
from mylightsystems.models import BatteryDevice

async def energy_dashboard():
    """Create a comprehensive energy monitoring dashboard."""
    async with MyLightSystemsApiClient() as client:
        auth = await client.auth("email", "password")

        # Get system overview
        profile = await client.get_profile(auth.token)
        devices = await client.get_devices(auth.token)
        states = await client.get_states(auth.token)

        print(f"🏠 Energy Dashboard - {profile.city}, {profile.country}")
        print(f"⚡ Grid Type: {profile.grid_type}")
        print(f"📅 Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        # Device summary
        device_types = {}
        for device in devices:
            device_types[device.type] = device_types.get(device.type, 0) + 1

        print("📊 Device Summary:")
        type_names = {
            'mst': '🏠 Master', 'bat': '🔋 Battery', 'sw': '🔌 Relay',
            'cmp': '📊 Counter', 'gmd': '📈 Multi-Counter', 'vrt': '💻 Virtual', 'eth': '🌐 Ethernet'
        }
        for device_type, count in device_types.items():
            name = type_names.get(device_type, device_type)
            print(f"   {name}: {count} device{'s' if count != 1 else ''}")

        # Power analysis
        total_production = 0
        total_consumption = 0
        battery_status = []

        for state in states:
            for sensor in state.sensor_states:
                if sensor.measure.type == "electric_power":
                    power = sensor.measure.value
                    if power < 0:  # Production
                        total_production += abs(power)
                    elif power > 0:  # Consumption
                        total_consumption += power

        # Battery information
        for device in devices:
            if isinstance(device, BatteryDevice):
                battery_status.append({
                    'name': device.name,
                    'capacity': device.capacity,
                    'state': 'Active' if device.state else 'Inactive'
                })

        print("\n⚡ Power Summary:")
        print(f"   📈 Total Production: {total_production:.2f}W")
        print(f"   📉 Total Consumption: {total_consumption:.2f}W")
        print(f"   ⚖️ Net Balance: {total_production - total_consumption:.2f}W")

        if battery_status:
            print("\n🔋 Battery Status:")
            for battery in battery_status:
                print(f"   • {battery['name']}: {battery['capacity']}% ({battery['state']})")

asyncio.run(energy_dashboard())
```

### Smart Device Automation

```python
from mylightsystems.models import RelayDevice
from mylightsystems.exceptions import MyLightSystemsSwitchNotAllowedError

async def smart_automation():
    """Intelligent device control based on energy production."""
    async with MyLightSystemsApiClient() as client:
        auth = await client.auth("email", "password")

        # Get current system state
        devices = await client.get_devices(auth.token)
        states = await client.get_states(auth.token)

        # Calculate current production vs consumption
        net_production = 0
        for state in states:
            for sensor in state.sensor_states:
                if sensor.measure.type == "electric_power":
                    net_production -= sensor.measure.value  # Negative = production

        print(f"⚡ Current net production: {net_production:.2f}W")

        # Find controllable devices
        relay_devices = [d for d in devices if isinstance(d, RelayDevice)]

        if net_production > 500:  # Excess production > 500W
            print("☀️ Excess solar production detected - enabling devices")
            for device in relay_devices:
                try:
                    result = await client.switch(auth.token, device.id, True)
                    print(f"   ✅ Enabled {device.name}: {'ON' if result.state else 'FAILED'}")
                except MyLightSystemsSwitchNotAllowedError:
                    print(f"   ⚠️ Cannot control {device.name}")

        elif net_production < -200:  # Consuming > 200W more than producing
            print("🌙 Low production detected - disabling non-essential devices")
            for device in relay_devices:
                if "non-essential" in device.name.lower():  # Example logic
                    try:
                        result = await client.switch(auth.token, device.id, False)
                        print(f"   ⏸️ Disabled {device.name}: {'OFF' if not result.state else 'FAILED'}")
                    except MyLightSystemsSwitchNotAllowedError:
                        print(f"   ⚠️ Cannot control {device.name}")

asyncio.run(smart_automation())
```

### Device Health Monitoring

```python
async def health_monitor():
    """Monitor device health and report issues."""
    async with MyLightSystemsApiClient() as client:
        auth = await client.auth("email", "password")

        devices = await client.get_devices(auth.token)
        states = await client.get_states(auth.token)

        print("🏥 Device Health Monitor")
        print("=" * 40)

        # Create device lookup
        device_lookup = {d.id: d for d in devices}

        for state in states:
            device = device_lookup.get(state.device_id)
            if not device:
                continue

            print(f"\n🔍 {device.name} ({device.id})")

            # Check if device is online
            if not state.state:
                print("   ⚠️ OFFLINE - Device is not responding")
            else:
                print("   ✅ ONLINE")

            # Check reporting frequency
            if state.report_period > 300:  # > 5 minutes
                print(f"   🐌 SLOW REPORTING - {state.report_period}s intervals")

            # Check sensor data
            if not state.sensor_states:
                print("   📊 NO SENSORS - No sensor data available")
            else:
                for sensor in state.sensor_states:
                    # Check for stale data (example: older than 10 minutes)
                    import datetime
                    now = datetime.datetime.now()
                    if (now - sensor.measure.date).total_seconds() > 600:
                        print(f"   🕒 STALE DATA - {sensor.sensor_id} last updated: {sensor.measure.date}")

                    # Check for unusual values
                    if sensor.measure.type == "electric_power" and abs(sensor.measure.value) > 10000:
                        print(f"   ⚡ HIGH POWER - {sensor.sensor_id}: {sensor.measure.value}W")

asyncio.run(health_monitor())
```

---

## 🔄 Retry and Resilience Patterns

### Automatic Retry with Exponential Backoff

```python
import asyncio
from mylightsystems.exceptions import MyLightSystemsConnectionError

async def retry_with_backoff(operation, max_retries=3, base_delay=1):
    """Retry an operation with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await operation()
        except MyLightSystemsConnectionError as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            print(f"⏳ Attempt {attempt + 1} failed, retrying in {delay}s...")
            await asyncio.sleep(delay)

# Usage
async def main():
    async with MyLightSystemsApiClient() as client:
        auth = await retry_with_backoff(
            lambda: client.auth("email", "password")
        )

        devices = await retry_with_backoff(
            lambda: client.get_devices(auth.token)
        )
```

### Session Management with Auto-Renewal

```python
class ManagedSession:
    """Automatically handle token renewal."""

    def __init__(self, client, email, password):
        self.client = client
        self.email = email
        self.password = password
        self.auth = None

    async def get_token(self):
        """Get valid token, refreshing if necessary."""
        if not self.auth:
            self.auth = await self.client.auth(self.email, self.password)
        return self.auth.token

    async def call_api(self, method, *args, **kwargs):
        """Call API method with automatic token renewal."""
        try:
            token = await self.get_token()
            return await method(token, *args, **kwargs)
        except MyLightSystemsUnauthorizedError:
            # Token expired, get new one
            self.auth = await self.client.auth(self.email, self.password)
            token = self.auth.token
            return await method(token, *args, **kwargs)

# Usage
async with MyLightSystemsApiClient() as client:
    session = ManagedSession(client, "email", "password")

    # These calls will automatically handle token renewal
    devices = await session.call_api(client.get_devices)
    states = await session.call_api(client.get_states)
```

---

## 🎯 Use Cases

### Home Energy Management System

Perfect for building energy management dashboards that:
- Monitor real-time energy production and consumption
- Control devices based on solar production
- Track battery charge levels and optimize usage
- Generate energy efficiency reports

### IoT Integration

Integrate with home automation platforms:
- Home Assistant custom components
- OpenHAB bindings
- Node-RED flows
- Custom IoT dashboards

### Energy Analytics

Build analytics applications for:
- Historical energy usage analysis
- Solar production forecasting
- Cost optimization recommendations
- Grid interaction monitoring

---

## 📞 Support & Resources

- **📖 API Documentation**: Complete endpoint reference above
- **🔧 Examples**: Real-world usage patterns and code samples
- **🐛 Issues**: [GitHub Issues](https://github.com/acesyde/python-mylight-systems-api-client/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/acesyde/python-mylight-systems-api-client/discussions)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../.github/LICENSE.md) file for details.

**MyLight Systems** is a trademark of MyLight Systems SAS. This is an unofficial client library.
