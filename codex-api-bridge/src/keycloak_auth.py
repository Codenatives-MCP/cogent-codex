import logging
from typing import Any, Dict

import httpx

from .config import settings

logger = logging.getLogger(__name__)


class KeycloakIntrospectionError(RuntimeError):
    """Raised when Keycloak token introspection fails."""


async def introspect_token(token: str) -> Dict[str, Any]:
    """Call Keycloak token introspection endpoint."""
    url = settings.get_keycloak_introspection_url()
    timeout = settings.keycloak_timeout_seconds
    data = {
        "token": token,
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, data=data)
    except httpx.HTTPError as exc:
        logger.error("Keycloak introspection request failed: %s", type(exc).__name__)
        raise KeycloakIntrospectionError("Keycloak introspection request failed") from exc

    if response.status_code < 200 or response.status_code >= 300:
        logger.warning("Keycloak introspection failed with status: %s", response.status_code)
        raise KeycloakIntrospectionError("Keycloak introspection failed")

    try:
        return response.json()
    except ValueError as exc:
        logger.warning("Keycloak introspection returned invalid JSON")
        raise KeycloakIntrospectionError("Keycloak introspection invalid JSON") from exc
