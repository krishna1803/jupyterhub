from __future__ import annotations

import httpx
from typing import Any, Dict, Optional, List
from ..settings import settings


class HubClient:
    """Async client for interacting with JupyterHub REST API.

    Wraps a single persistent httpx.AsyncClient with auth headers.
    """

    def __init__(self, base_url: Optional[str] = None, api_token: Optional[str] = None, verify: Optional[bool] = None):
        self._base_url = (base_url or str(settings.jupyterhub_url)).rstrip("/")
        self._api_token = api_token or settings.api_token
        self._verify = settings.verify_ssl if verify is None else verify
        self._client = httpx.AsyncClient(
            base_url=self._base_url + "/hub/api",
            headers={"Authorization": f"token {self._api_token}"},
            timeout=settings.request_timeout,
            verify=self._verify,
        )

    async def close(self):
        await self._client.aclose()

    # Generic HTTP helpers -------------------------------------------------
    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        resp = await self._client.request(method, path, **kwargs)
        resp.raise_for_status()
        return resp

    async def get(self, path: str, **kwargs) -> Any:
        return (await self._request("GET", path, **kwargs)).json()

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return (await self._request("POST", path, json=json, **kwargs)).json()

    async def delete(self, path: str, **kwargs) -> Any:
        resp = await self._request("DELETE", path, **kwargs)
        if resp.content:
            return resp.json()
        return {"status": "deleted"}

    async def patch(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return (await self._request("PATCH", path, json=json, **kwargs)).json()

    # High-level endpoints (comprehensive) ---------------------------------------
    
    # Health & Info
    async def get_health(self):
        """Get hub health status"""
        try:
            return await self.get("/health")
        except httpx.HTTPStatusError as e:
            return {"status": "error", "detail": str(e)}

    async def get_info(self):
        """Get hub info including version"""
        return await self.get("/info")

    # Users
    async def list_users(self):
        """List all users"""
        return await self.get("/users")

    async def get_user(self, name: str):
        """Get specific user details"""
        return await self.get(f"/users/{name}")

    async def create_user(self, name: str, admin: bool = False):
        """Create a new user"""
        return await self.post("/users", json={"name": name, "admin": admin})

    async def delete_user(self, name: str):
        """Delete a user"""
        return await self.delete(f"/users/{name}")

    async def modify_user(self, name: str, admin: Optional[bool] = None):
        """Modify user properties"""
        data = {}
        if admin is not None:
            data["admin"] = admin
        return await self.patch(f"/users/{name}", json=data)

    # Servers
    async def list_servers(self, user: str):
        """List user's servers"""
        user_data = await self.get(f"/users/{user}")
        return user_data.get("servers", {})

    async def get_server(self, user: str, server_name: str = ""):
        """Get specific server details"""
        return await self.get(f"/users/{user}/servers/{server_name}")

    async def start_server(self, user: str, server_name: str = "", options: Optional[Dict[str, Any]] = None):
        """Start a server for user"""
        json_data = options or {}
        return await self.post(f"/users/{user}/servers/{server_name}", json=json_data)

    async def stop_server(self, user: str, server_name: str = ""):
        """Stop a server for user"""
        return await self.delete(f"/users/{user}/servers/{server_name}")

    # Groups
    async def list_groups(self):
        """List all groups"""
        return await self.get("/groups")

    async def get_group(self, name: str):
        """Get specific group details"""
        return await self.get(f"/groups/{name}")

    async def create_group(self, name: str, users: Optional[List[str]] = None):
        """Create a new group"""
        data = {"name": name}
        if users:
            data["users"] = users
        return await self.post("/groups", json=data)

    async def delete_group(self, name: str):
        """Delete a group"""
        return await self.delete(f"/groups/{name}")

    async def add_user_to_group(self, group_name: str, username: str):
        """Add user to group"""
        return await self.post(f"/groups/{group_name}/users", json={"users": [username]})

    async def remove_user_from_group(self, group_name: str, username: str):
        """Remove user from group"""
        return await self.delete(f"/groups/{group_name}/users/{username}")

    # Services
    async def list_services(self):
        """List all services"""
        return await self.get("/services")

    async def get_service(self, name: str):
        """Get specific service details"""
        return await self.get(f"/services/{name}")

    # Tokens
    async def list_tokens(self):
        """List all tokens (admin only)"""
        return await self.get("/tokens")

    async def get_token(self, token_id: str):
        """Get specific token details"""
        return await self.get(f"/tokens/{token_id}")

    async def create_token(self, user: str, note: Optional[str] = None, expires_in: Optional[int] = None):
        """Create API token for user"""
        data = {}
        if note:
            data["note"] = note
        if expires_in:
            data["expires_in"] = expires_in
        return await self.post(f"/users/{user}/tokens", json=data)

    async def delete_token(self, user: str, token_id: str):
        """Delete a user's token"""
        return await self.delete(f"/users/{user}/tokens/{token_id}")

    # Admin operations
    async def shutdown_hub(self):
        """Shutdown the hub (admin only)"""
        return await self.post("/shutdown")

    async def get_proxy(self):
        """Get proxy information"""
        return await self.get("/proxy")

    async def force_proxy_check(self):
        """Force proxy to check routes"""
        return await self.post("/proxy")

    # Spawner operations
    async def cull_servers(self):
        """Cull idle servers"""
        return await self.post("/cull")

    # Activity tracking
    async def user_activity(self, user: str, servers: Optional[List[str]] = None):
        """Update user activity"""
        data = {}
        if servers:
            data["servers"] = servers
        return await self.post(f"/users/{user}/activity", json=data)
