from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from ..settings import settings
from ..client.base import HubClient
from ..models import (
    UserModel, CreateUserRequest, ServerModel, GroupModel, 
    CreateGroupRequest, TokenModel, CreateTokenRequest, HealthModel
)

app = FastAPI(
    title="JupyterHub Manager API", 
    version="0.1.0",
    description="Professional API for managing JupyterHub instances",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_client():
    client = HubClient()
    try:
        yield client
    finally:
        await client.close()


# Health & Info endpoints
@app.get("/health", tags=["system"], response_model=HealthModel)
async def health(client: HubClient = Depends(get_client)):
    """Get JupyterHub health status"""
    return await client.get_health()


@app.get("/info", tags=["system"])
async def hub_info(client: HubClient = Depends(get_client)):
    """Get JupyterHub information"""
    return await client.get_info()


# User management endpoints
@app.get("/users", tags=["users"], response_model=List[UserModel])
async def list_users(client: HubClient = Depends(get_client)):
    """List all users"""
    return await client.list_users()


@app.get("/users/{username}", tags=["users"], response_model=UserModel)
async def get_user(username: str, client: HubClient = Depends(get_client)):
    """Get specific user details"""
    try:
        return await client.get_user(username)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User {username} not found")


@app.post("/users", tags=["users"], status_code=201, response_model=UserModel)
async def create_user(user_data: CreateUserRequest, client: HubClient = Depends(get_client)):
    """Create a new user"""
    return await client.create_user(user_data.name, user_data.admin)


@app.delete("/users/{username}", tags=["users"], status_code=204)
async def delete_user(username: str, client: HubClient = Depends(get_client)):
    """Delete a user"""
    await client.delete_user(username)
    return {"status": "deleted"}


@app.patch("/users/{username}", tags=["users"], response_model=UserModel)
async def modify_user(username: str, admin: Optional[bool] = None, client: HubClient = Depends(get_client)):
    """Modify user properties"""
    return await client.modify_user(username, admin=admin)


# Server management endpoints
@app.get("/users/{username}/servers", tags=["servers"])
async def list_user_servers(username: str, client: HubClient = Depends(get_client)):
    """List user's servers"""
    return await client.list_servers(username)


@app.get("/users/{username}/servers/{server_name}", tags=["servers"], response_model=ServerModel)
async def get_server(username: str, server_name: str = "", client: HubClient = Depends(get_client)):
    """Get specific server details"""
    return await client.get_server(username, server_name)


@app.post("/users/{username}/servers/{server_name}", tags=["servers"], status_code=201)
async def start_server(username: str, server_name: str = "", client: HubClient = Depends(get_client)):
    """Start a server for user"""
    return await client.start_server(username, server_name)


@app.delete("/users/{username}/servers/{server_name}", tags=["servers"], status_code=202)
async def stop_server(username: str, server_name: str = "", client: HubClient = Depends(get_client)):
    """Stop a server for user"""
    return await client.stop_server(username, server_name)


# Group management endpoints
@app.get("/groups", tags=["groups"], response_model=List[GroupModel])
async def list_groups(client: HubClient = Depends(get_client)):
    """List all groups"""
    return await client.list_groups()


@app.get("/groups/{group_name}", tags=["groups"], response_model=GroupModel)
async def get_group(group_name: str, client: HubClient = Depends(get_client)):
    """Get specific group details"""
    return await client.get_group(group_name)


@app.post("/groups", tags=["groups"], status_code=201, response_model=GroupModel)
async def create_group(group_data: CreateGroupRequest, client: HubClient = Depends(get_client)):
    """Create a new group"""
    return await client.create_group(group_data.name, group_data.users)


@app.delete("/groups/{group_name}", tags=["groups"], status_code=204)
async def delete_group(group_name: str, client: HubClient = Depends(get_client)):
    """Delete a group"""
    await client.delete_group(group_name)
    return {"status": "deleted"}


@app.post("/groups/{group_name}/users", tags=["groups"])
async def add_user_to_group(group_name: str, username: str, client: HubClient = Depends(get_client)):
    """Add user to group"""
    return await client.add_user_to_group(group_name, username)


@app.delete("/groups/{group_name}/users/{username}", tags=["groups"], status_code=204)
async def remove_user_from_group(group_name: str, username: str, client: HubClient = Depends(get_client)):
    """Remove user from group"""
    await client.remove_user_from_group(group_name, username)
    return {"status": "removed"}


# Service endpoints
@app.get("/services", tags=["services"])
async def list_services(client: HubClient = Depends(get_client)):
    """List all services"""
    return await client.list_services()


@app.get("/services/{service_name}", tags=["services"])
async def get_service(service_name: str, client: HubClient = Depends(get_client)):
    """Get specific service details"""
    return await client.get_service(service_name)


# Token management endpoints
@app.get("/tokens", tags=["tokens"], response_model=List[TokenModel])
async def list_tokens(client: HubClient = Depends(get_client)):
    """List all tokens (admin only)"""
    return await client.list_tokens()


@app.post("/users/{username}/tokens", tags=["tokens"], status_code=201, response_model=TokenModel)
async def create_token(username: str, token_data: CreateTokenRequest, client: HubClient = Depends(get_client)):
    """Create API token for user"""
    return await client.create_token(username, token_data.note, token_data.expires_in)


@app.delete("/users/{username}/tokens/{token_id}", tags=["tokens"], status_code=204)
async def delete_token(username: str, token_id: str, client: HubClient = Depends(get_client)):
    """Delete a user's token"""
    await client.delete_token(username, token_id)
    return {"status": "deleted"}


# Admin endpoints
@app.post("/admin/shutdown", tags=["admin"])
async def shutdown_hub(client: HubClient = Depends(get_client)):
    """Shutdown the hub (admin only)"""
    return await client.shutdown_hub()


@app.get("/admin/proxy", tags=["admin"])
async def get_proxy_info(client: HubClient = Depends(get_client)):
    """Get proxy information"""
    return await client.get_proxy()


@app.post("/admin/cull", tags=["admin"])
async def cull_servers(client: HubClient = Depends(get_client)):
    """Cull idle servers"""
    return await client.cull_servers()
