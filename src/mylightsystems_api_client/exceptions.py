"""Exceptions for MyLightSystems API Client."""


class MyLightSystemsError(Exception):
    """Generic exception."""


class MyLightSystemsConnectionError(MyLightSystemsError):
    """Connection error."""
