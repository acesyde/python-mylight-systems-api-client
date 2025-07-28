# Get User Profile

[← Authentication](auth.md) | [Back to Documentation](index.md) | [Next: Get Devices →](get_devices.md)

Retrieve the authenticated user's profile information.

## Method

```python
async def get_profile(self, auth_token: str) -> Profile
```

## Description

Fetches detailed profile information for the authenticated user, including personal details, location, and account settings.

## Parameters

| Parameter    | Type  | Required | Description                                        |
| ------------ | ----- | -------- | -------------------------------------------------- |
| `auth_token` | `str` | Yes      | Authentication token obtained from [auth](auth.md) |

## Returns

Returns a [`Profile`](models.md#profile) object containing:
- `id` (int): User ID
- `grid_type` (str): Electrical grid configuration type
- `tenant` (str): Tenant/organization identifier
- `city` (str): User's city
- `country` (str): User's country (ISO country code)
- `postal_code` (str): Postal/ZIP code
- `address` (str): Street address

## Sample Usage

```python
import asyncio
from mylightsystems.client import MyLightSystemsApiClient

async def main():
    async with MyLightSystemsApiClient() as client:
        # First authenticate
        auth = await client.auth("user@example.com", "password")

        # Get profile
        try:
            profile = await client.get_profile(auth.token)
            print(f"User ID: {profile.id}")
            print(f"Location: {profile.city}, {profile.country}")
            print(f"Grid Type: {profile.grid_type}")
            print(f"Address: {profile.address}")
        except MyLightSystemsUnauthorizedError:
            print("Token expired or invalid")

asyncio.run(main())
```

## Sample Response

```json
{
    "status": "ok",
    "tenant": "myhome",
    "id": "fake_user_id",
    "email": "fake_email@fake.fr",
    "firstName": "fake_firstname",
    "lastName": "fake_lastname",
    "latitude": "45.01",
    "longitude": "-0.80",
    "postalCode": "11111",
    "city": "Lourdes",
    "country": "FR",
    "address": "10 rue de la gare",
    "gridType": "1 phase",
    "currency": "EUR",
    "electricityProvider": "Mylight Systems"
}
```

The response is automatically parsed into a `Profile` object:

```python
Profile(
    id="fake_user_id",
    grid_type="1 phase",
    tenant="myhome",
    city="Lourdes",
    country="FR",
    postal_code="11111",
    address="10 rue de la gare"
)
```

## Exceptions

This method can raise the following exceptions:

### MyLightSystemsUnauthorizedError
Raised when the authentication token is invalid or expired.

```python
from mylightsystems.exceptions import MyLightSystemsUnauthorizedError

try:
    profile = await client.get_profile("invalid_token")
except MyLightSystemsUnauthorizedError:
    print("Authentication token is invalid or expired")
```

### MyLightSystemsConnectionError
Raised when there's a network connection issue:
- Timeout (default: 10 seconds)
- Network unreachable
- DNS resolution failure

```python
from mylightsystems.exceptions import MyLightSystemsConnectionError

try:
    profile = await client.get_profile(auth.token)
except MyLightSystemsConnectionError:
    print("Failed to connect to API")

## See Also

- [Authentication](auth.md) - How to get the required token
- [Get Devices](get_devices.md) - Next step: list user devices
- [Data Models: Profile](models.md#profile) - Profile object reference
- [Exception Handling](exceptions.md) - Error handling patterns
```
