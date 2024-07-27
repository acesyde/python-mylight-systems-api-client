"""Models for MyLightSystems API Client."""

from dataclasses import dataclass


@dataclass
class Login:
    """Login model."""

    token: str


@dataclass
class Profile:
    """Profile model."""

    id: int
    grid_type: str
