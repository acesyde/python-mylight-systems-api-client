# Authentication

[← Back to Documentation](index.md) | [Next: Get Profile →](get_profile.md)

Login to the MyLightSystems API and obtain an authentication token.

## Method

```python
async def auth(self, email: str, password: str) -> Auth
```

## Description

Authenticates a user with their email and password, returning an authentication token that must be used for subsequent API calls.

## Parameters

| Parameter  | Type  | Required | Description          |
| ---------- | ----- | -------- | -------------------- |
| `email`    | `str` | Yes      | User's email address |
| `password` | `str` | Yes      | User's password      |

## Returns

Returns an [`Auth`](models.md#auth) object containing:
- `token` (str): Authentication token for API requests

## Sample Usage

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient

async def main():
    async with MyLightSystemsApiClient() as client:
        try:
            auth = await client.auth("user@example.com", "password123")
            print(f"Authentication successful. Token: {auth.token}")
        except MyLightSystemsInvalidAuthError:
            print("Invalid email or password")
        except MyLightSystemsConnectionError:
            print("Connection failed")

asyncio.run(main())
```

## Sample Response

```json
{
    "status": "ok",
    "authToken": "fake_auth_token"
}
```

The response is automatically parsed into an `Auth` object:

```python
Auth(token="fake_auth_token")
```

## Exceptions

This method can raise the following exceptions:

### MyLightSystemsInvalidAuthError
Raised when the provided credentials are invalid. This includes:
- Invalid email/password combination
- Undefined email
- Undefined password

```python
from mylightsystems.exceptions import MyLightSystemsInvalidAuthError

try:
    auth = await client.auth("wrong@email.com", "wrongpassword")
except MyLightSystemsInvalidAuthError:
    print("Authentication failed: Invalid credentials")
```

### MyLightSystemsConnectionError
Raised when there's a network connection issue:
- Timeout (default: 10 seconds)
- Network unreachable
- DNS resolution failure

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError

try:
    auth = await client.auth("user@example.com", "password")
except MyLightSystemsConnectionError:
    print("Authentication failed: Connection error")
```

### MyLightSystemsUnauthorizedError
Raised when the API returns an "not.authorized" error.

```python
from mylightsystems.exceptions import MyLightSystemsUnauthorizedError

try:
    auth = await client.auth("user@example.com", "password")
except MyLightSystemsUnauthorizedError:
    print("Authentication failed: Unauthorized")

## See Also

- [Get User Profile](get_profile.md) - First step after authentication
- [Exception Handling](exceptions.md) - Complete error handling guide
- [Data Models: Auth](models.md#auth) - Auth object reference
- [Quick Start Guide](README.md#quick-start) - Complete example with authentication
```
