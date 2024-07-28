"""Exceptions for MyLightSystems API Client."""


class MyLightSystemsError(Exception):
    """Generic exception."""


class MyLightSystemsConnectionError(MyLightSystemsError):
    """Connection error."""


class MyLightSystemsInvalidAuthError(MyLightSystemsError):
    """Invalid authentication error."""


class MyLightSystemsUnauthorizedError(MyLightSystemsError):
    """Unauthorized error."""


class MyLightSystemsUnknownDeviceError(MyLightSystemsError):
    """Unknown device error."""
