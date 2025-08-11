import pytest
from unittest.mock import AsyncMock, patch
from jupyterhub_manager.client.base import HubClient


@pytest.mark.asyncio
async def test_hub_client_initialization():
    """Test HubClient initialization"""
    client = HubClient(
        base_url="https://test.hub.com",
        api_token="test-token",
        verify=False
    )
    
    assert client._base_url == "https://test.hub.com"
    assert client._api_token == "test-token"
    assert client._verify == False
    
    await client.close()


@pytest.mark.asyncio
async def test_user_operations():
    """Test user-related operations"""
    
    with patch('httpx.AsyncClient') as mock_client:
        # Setup mock responses
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {"name": "testuser", "admin": False}
        
        mock_client.return_value.request = AsyncMock(return_value=mock_response)
        
        client = HubClient()
        
        # Test create user
        result = await client.create_user("testuser", admin=False)
        assert result["name"] == "testuser"
        
        # Test get user
        result = await client.get_user("testuser")
        assert result["name"] == "testuser"
        
        await client.close()


@pytest.mark.asyncio
async def test_server_operations():
    """Test server-related operations"""
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {"ready": True, "url": "http://test.com"}
        
        mock_client.return_value.request = AsyncMock(return_value=mock_response)
        
        client = HubClient()
        
        # Test start server
        result = await client.start_server("testuser")
        assert "ready" in result
        
        # Test stop server
        mock_response.content = b'{"status": "deleted"}'
        result = await client.stop_server("testuser")
        assert result["ready"]  # Based on mock
        
        await client.close()


@pytest.mark.asyncio
async def test_group_operations():
    """Test group-related operations"""
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {"name": "testgroup", "users": []}
        
        mock_client.return_value.request = AsyncMock(return_value=mock_response)
        
        client = HubClient()
        
        # Test create group
        result = await client.create_group("testgroup", ["user1", "user2"])
        assert result["name"] == "testgroup"
        
        # Test list groups
        mock_response.json.return_value = [{"name": "group1"}, {"name": "group2"}]
        result = await client.list_groups()
        assert len(result) == 2
        
        await client.close()


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in client"""
    
    with patch('httpx.AsyncClient') as mock_client:
        import httpx
        
        # Simulate HTTP error
        mock_client.return_value.request.side_effect = httpx.HTTPStatusError(
            "Not found", request=AsyncMock(), response=AsyncMock()
        )
        
        client = HubClient()
        
        # Test health check with error
        result = await client.get_health()
        assert result["status"] == "error"
        
        await client.close()


@pytest.mark.asyncio
async def test_token_operations():
    """Test token-related operations"""
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {"token": "abc123", "user": "testuser"}
        
        mock_client.return_value.request = AsyncMock(return_value=mock_response)
        
        client = HubClient()
        
        # Test create token
        result = await client.create_token("testuser", "test note", 3600)
        assert result["token"] == "abc123"
        
        await client.close()
