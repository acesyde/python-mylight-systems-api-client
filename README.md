# Python: MyLight Systems API Client

[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](.github/LICENSE.md)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]

Asynchronous Python client for the MyLight Systems API, enabling programmatic control and monitoring of MyLight Systems solar energy and home automation devices.

## Features

🔋 **Device Management** - Control and monitor solar panels, batteries, relays, and sensors
⚡ **Real-time Data** - Get live power consumption, production, and device states
🏠 **Home Automation** - Switch devices on/off and automate energy management
📊 **Energy Monitoring** - Track total energy production, consumption, and efficiency metrics
🔐 **Secure Authentication** - Token-based API authentication with error handling
🚀 **Async/Await** - Built for modern Python with full async support

## Installation

Install from PyPI:

```bash
pip install mylightsystems
```

## Quick Start

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient

async def main():
    async with MyLightSystemsApiClient() as client:
        # Authenticate
        auth = await client.auth("your_email@example.com", "your_password")

        # Get user profile
        profile = await client.get_profile(auth.token)
        print(f"User: {profile.id} in {profile.city}, {profile.country}")

        # Get all devices
        devices = await client.get_devices(auth.token)
        print(f"Found {len(devices)} devices")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Overview

The client provides methods to interact with all major MyLight Systems endpoints:

| Method | Description | Documentation |
|--------|-------------|---------------|
| `auth(email, password)` | Authenticate and get access token | [📖 Auth](docs/auth.md) |
| `get_profile(token)` | Get user profile information | [📖 Profile](docs/get_profile.md) |
| `get_devices(token)` | List all connected devices | [📖 Devices](docs/get_devices.md) |
| `get_states(token)` | Get real-time device states and sensor data | [📖 States](docs/get_states.md) |
| `get_measures_total(token, device_id)` | Get total energy measures for a device | [📖 Measures](docs/get_measures_total.md) |
| `switch(token, device_id, state)` | Control device on/off state | [📖 Switch](docs/switch.md) |

## Device Types

The library supports all MyLight Systems device types:

- **🏠 Master Device** (`mst`) - Main control unit
- **🔋 Battery Device** (`bat`) - Energy storage systems
- **🔌 Relay Device** (`sw`) - Controllable switches and outlets
- **📊 Counter Device** (`cmp`) - Energy measurement devices
- **📈 Composite Counter** (`gmd`) - Multi-phase energy meters
- **💻 Virtual Device** (`vrt`) - Software-defined devices
- **🌐 Ethernet Device** (`eth`) - Network-connected devices

Each device type has specific properties and capabilities. See the [Device Models](docs/models.md) documentation for complete details.

## Documentation

📚 **[Complete API Documentation](docs/index.md)** - Comprehensive guide with examples and advanced usage patterns

### Quick Links
- **[Getting Started](docs/index.md#quick-start)** - Complete setup and usage examples
- **[Advanced Usage](docs/index.md#advanced-usage)** - Energy monitoring, automation, and health monitoring
- **[Error handling](docs/index.md#error-handling)** - Comprehensive error handling patterns
- **[Retry Patterns](docs/index.md#retry-and-resilience-patterns)** - Production-ready resilience strategies

### API Reference
- [Authentication](docs/auth.md) - Login and token management
- [User Profile](docs/get_profile.md) - Get account information
- [Device Management](docs/get_devices.md) - List and identify devices
- [Device States](docs/get_states.md) - Real-time monitoring
- [Energy Measures](docs/get_measures_total.md) - Total energy data
- [Device Control](docs/switch.md) - Switch devices on/off

### Reference Guides
- [Data Models](docs/models.md) - All data structures and fields
- [Exception Handling](docs/exceptions.md) - Error types and handling patterns

## Use Cases

Perfect for building:

🏠 **Home Energy Management** - Real-time monitoring dashboards and automated energy optimization
🔌 **IoT Integration** - Home Assistant components, OpenHAB bindings, Node-RED flows
📊 **Energy Analytics** - Historical analysis, solar forecasting, cost optimization
🤖 **Smart Automation** - Intelligent device control based on production and consumption

See the [complete documentation](docs/index.md) for detailed examples and implementation patterns.

## Requirements

- Python 3.8+
- aiohttp
- Modern async/await support

## Contributing

We welcome contributions! This project uses modern Python development tools:

- **[mise](https://mise.jdx.dev/)** for tool management
- **[uv](https://docs.astral.sh/uv/)** for dependency management
- **[ruff](https://docs.astral.sh/ruff/)** for linting and formatting
- **[pre-commit](https://pre-commit.com/)** for automated checks

### Development Setup

```bash
# Install mise for tool management
curl https://mise.run | sh

# Set up the project
mise install
mise run project:setup
```

### Development Commands

```bash
# Run all checks and tests
mise run precommit:run

# Run tests only
mise run project:tests

# Run linting
mise run project:lint

# Fix linting issues
mise run project:lint-fix
```

See our [Contributing Guidelines](.github/CONTRIBUTING.md) for detailed information.

## Authors & Contributors

Created and maintained by [Pierre-Emmanuel Mercier][acesyde].

For a full list of contributors, see [the contributor's page][contributors].

## License

This project is licensed under the MIT License - see the [LICENSE](.github/LICENSE.md) file for details.

---

**MyLight Systems** is a trademark of MyLight Systems SAS. This project is an unofficial client library and is not affiliated with or endorsed by MyLight Systems SAS.

[build-shield]: https://github.com/acesyde/python-mylight-systems-api-client/actions/workflows/tests.yaml/badge.svg
[build]: https://github.com/acesyde/python-mylight-systems-api-client/actions
[codecov-shield]: https://codecov.io/gh/acesyde/python-mylight-systems-api-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/acesyde/python-mylight-systems-api-client
[contributors]: https://github.com/acesyde/python-mylight-systems-api-client/graphs/contributors
[acesyde]: https://github.com/acesyde
[license-shield]: https://img.shields.io/github/license/acesyde/python-mylight-systems-api-client.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-stable-green.svg
[python-versions-shield]: https://img.shields.io/pypi/pyversions/mylightsystems
[releases-shield]: https://img.shields.io/github/release/acesyde/python-mylight-systems-api-client.svg
[releases]: https://github.com/acesyde/python-mylight-systems-api-client/releases
[pypi]: https://pypi.org/project/mylightsystems/
