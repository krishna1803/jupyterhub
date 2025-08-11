import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from jupyterhub_manager.api.main import app
from jupyterhub_manager.client.base import HubClient


@pytest.fixture
def mock_client():
    """Mock HubClient for testing"""
    client = AsyncMock(spec=HubClient)
    return client


@pytest.mark.asyncio
async def test_comprehensive_user_operations(mock_client):
    """Test comprehensive user operations"""
    
    # Mock responses
    mock_client.list_users.return_value = [
        {"name": "alice", "admin": False, "servers": {}},
        {"name": "bob", "admin": True, "servers": {"": {"ready": True}}}
    ]
    mock_client.get_user.return_value = {"name": "alice", "admin": False}
    mock_client.create_user.return_value = {"name": "charlie", "admin": False}
    mock_client.modify_user.return_value = {"name": "alice", "admin": True}
    
    with patch('jupyterhub_manager.api.main.get_client') as mock_get_client:
        mock_get_client.return_value.__aenter__.return_value = mock_client
        mock_get_client.return_value.__aexit__.return_value = None
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Test list users
            response = await ac.get("/users")
            assert response.status_code == 200
            users = response.json()
            assert len(users) == 2
            assert users[0]["name"] == "alice"
            
            # Test get user
            response = await ac.get("/users/alice")
            assert response.status_code == 200
            assert response.json()["name"] == "alice"
            
            # Test create user
            response = await ac.post("/users", json={"name": "charlie", "admin": False})
            assert response.status_code == 201
            assert response.json()["name"] == "charlie"
            
            # Test modify user
            response = await ac.patch("/users/alice?admin=true")
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_server_management(mock_client):
    """Test server management operations"""
    
    mock_client.list_servers.return_value = {"": {"ready": True, "url": "http://example.com"}}
    mock_client.get_server.return_value = {"ready": True, "url": "http://example.com"}
    mock_client.start_server.return_value = {"pending": "spawn"}
    mock_client.stop_server.return_value = {"status": "deleted"}
    
    with patch('jupyterhub_manager.api.main.get_client') as mock_get_client:
        mock_get_client.return_value.__aenter__.return_value = mock_client
        mock_get_client.return_value.__aexit__.return_value = None
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Test list servers
            response = await ac.get("/users/alice/servers")
            assert response.status_code == 200
            
            # Test start server
            response = await ac.post("/users/alice/servers/")
            assert response.status_code == 201
            
            # Test stop server
            response = await ac.delete("/users/alice/servers/")
            assert response.status_code == 202


@pytest.mark.asyncio
async def test_group_operations(mock_client):
    """Test group management operations"""
    
    mock_client.list_groups.return_value = [{"name": "scientists", "users": ["alice", "bob"]}]
    mock_client.create_group.return_value = {"name": "newgroup", "users": []}
    mock_client.add_user_to_group.return_value = {"status": "added"}
    
    with patch('jupyterhub_manager.api.main.get_client') as mock_get_client:
        mock_get_client.return_value.__aenter__.return_value = mock_client
        mock_get_client.return_value.__aexit__.return_value = None
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Test list groups
            response = await ac.get("/groups")
            assert response.status_code == 200
            
            # Test create group
            response = await ac.post("/groups", json={"name": "newgroup", "users": []})
            assert response.status_code == 201


@pytest.mark.asyncio
async def test_admin_operations(mock_client):
    """Test admin operations"""
    
    mock_client.get_proxy.return_value = {"routes": {}}
    mock_client.cull_servers.return_value = {"culled": 3}
    
    with patch('jupyterhub_manager.api.main.get_client') as mock_get_client:
        mock_get_client.return_value.__aenter__.return_value = mock_client
        mock_get_client.return_value.__aexit__.return_value = None
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Test proxy info
            response = await ac.get("/admin/proxy")
            assert response.status_code == 200
            
            # Test cull servers
            response = await ac.post("/admin/cull")
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_error_handling(mock_client):
    """Test error handling"""
    
    mock_client.get_user.side_effect = Exception("User not found")
    
    with patch('jupyterhub_manager.api.main.get_client') as mock_get_client:
        mock_get_client.return_value.__aenter__.return_value = mock_client
        mock_get_client.return_value.__aexit__.return_value = None
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Test user not found
            response = await ac.get("/users/nonexistent")
            assert response.status_code == 404
