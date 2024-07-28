"""Device factory for MyLightSystems API."""

from __future__ import annotations

from dataclasses import fields
from typing import Any

from mylightsystems.exceptions import MyLightSystemsUnknownDeviceError
from mylightsystems.models import (
    BatteryDevice,
    CompositeCounterDevice,
    CounterDevice,
    Device,
    MasterDevice,
    RelayDevice,
    VirtualDevice,
)

# Mapping from type name to class
device_type_mapping: dict[str, type[Device]] = {
    "bat": BatteryDevice,
    "sw": RelayDevice,
    "cmp": CounterDevice,
    "gmd": CompositeCounterDevice,
    "vrt": VirtualDevice,
    "mst": MasterDevice,
}

device_property_mapping: dict[str, str] = {
    "id": "id",
    "name": "name",
    "type": "type",
    "state": "state",
}


class DeviceFactory:
    """Device factory."""

    def __init__(self) -> None:
        """Device factory initializer."""
        self.type_mapping = {
            "bat": BatteryDevice,
            "sw": RelayDevice,
            "cmp": CounterDevice,
            "gmd": CompositeCounterDevice,
            "vrt": VirtualDevice,
            "mst": MasterDevice,
        }
        self.field_mapping = {
            "deviceTypeId": "type_id",
            "masterMac": "master_id",
            "masterType": "master_type",
            "reportPeriod": "report_period",
            "batteryCapacity": "capacity",
        }
        self.value_transformers = {
            "state": lambda x: x.lower() == "on",
        }

    def create_device(self, data: dict[str, Any]) -> Device:
        """Create a new device."""
        device_type = data.get("type", "device").lower()
        device_class = self.type_mapping.get(device_type, None)

        if device_class is None:
            raise MyLightSystemsUnknownDeviceError(device_type)

        # Get the fields of the device class
        class_fields = {field.name for field in fields(device_class)}

        # Create a dictionary with only the relevant fields
        device_data = {}
        for json_field, value in data.items():
            class_field = self.field_mapping.get(json_field, json_field)
            if class_field in class_fields:
                # Apply value transformation if needed
                if class_field in self.value_transformers:
                    value = self.value_transformers[class_field](value)
                device_data[class_field] = value

        return device_class(**device_data)
