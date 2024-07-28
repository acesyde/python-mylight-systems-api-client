"""Models for MyLightSystems API Client."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Auth:
    """Auth model."""

    token: str


@dataclass
class Profile:
    """Profile model."""

    id: int
    grid_type: str


@dataclass
class Device:
    """Device model."""

    id: str
    name: str
    type: str
    type_id: str


@dataclass
class BatteryDevice(Device):
    """Represent a battery."""

    state: bool
    capacity: int


@dataclass
class RelayDevice(Device):
    """Represent a relay."""

    state: bool
    master_id: str
    master_type: str


@dataclass
class CounterDevice(Device):
    """Represent a counter."""

    state: bool
    phase: int
    master_id: str
    master_type: str


@dataclass
class CompositeCounterDevice(Device):
    """Represent a composite counter."""

    master_id: str
    master_type: str
    children: dict[str, int]


@dataclass
class VirtualDevice(Device):
    """Represent a virtual."""

    state: bool


@dataclass
class MasterDevice(Device):
    """Represent a master."""

    state: bool
    report_period: int
