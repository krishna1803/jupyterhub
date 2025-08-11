from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserModel(BaseModel):
    """User model from JupyterHub API"""
    name: str
    admin: bool = False
    groups: List[str] = []
    server: Optional[str] = None
    pending: Optional[str] = None
    created: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    servers: Dict[str, Any] = {}


class ServerModel(BaseModel):
    """Server model from JupyterHub API"""
    name: str = ""
    ready: bool = False
    pending: Optional[str] = None
    url: Optional[str] = None
    progress_url: Optional[str] = None
    started: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    state: Dict[str, Any] = {}
    user_options: Dict[str, Any] = {}


class GroupModel(BaseModel):
    """Group model from JupyterHub API"""
    name: str
    users: List[str] = []
    properties: Dict[str, Any] = {}


class ServiceModel(BaseModel):
    """Service model from JupyterHub API"""
    name: str
    admin: bool = False
    url: Optional[str] = None
    prefix: Optional[str] = None
    pid: Optional[int] = None
    command: Optional[List[str]] = None


class TokenModel(BaseModel):
    """API Token model"""
    token: str
    id: Optional[str] = None
    user: Optional[str] = None
    service: Optional[str] = None
    roles: List[str] = []
    scopes: List[str] = []
    note: Optional[str] = None
    created: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class HealthModel(BaseModel):
    """Health check response"""
    status: str = "ok"
    version: Optional[str] = None
    detail: Optional[str] = None


class CreateUserRequest(BaseModel):
    """Request model for creating a user"""
    name: str = Field(..., description="Username")
    admin: bool = Field(False, description="Whether user should be admin")


class CreateGroupRequest(BaseModel):
    """Request model for creating a group"""
    name: str = Field(..., description="Group name")
    users: List[str] = Field([], description="Initial users in group")


class CreateTokenRequest(BaseModel):
    """Request model for creating an API token"""
    note: Optional[str] = Field(None, description="Note about the token")
    expires_in: Optional[int] = Field(None, description="Token expiration in seconds")
    roles: List[str] = Field([], description="Roles for the token")
    scopes: List[str] = Field([], description="Scopes for the token")


class ServerOptions(BaseModel):
    """Server spawn options"""
    image: Optional[str] = None
    cpu_limit: Optional[float] = None
    mem_limit: Optional[str] = None
    env: Dict[str, str] = {}
