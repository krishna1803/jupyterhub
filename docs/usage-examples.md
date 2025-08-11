# Usage Examples

## Python Client Examples

### Basic User Management

```python
import asyncio
from jupyterhub_manager.client.base import HubClient

async def main():
    client = HubClient(
        base_url="https://your-hub.example.com",
        api_token="your-admin-token"
    )
    
    try:
        # List users
        users = await client.list_users()
        print(f"Found {len(users)} users")
        
        # Create a new user
        new_user = await client.create_user("alice", admin=False)
        print(f"Created user: {new_user['name']}")
        
        # Start server for user
        server = await client.start_server("alice")
        print(f"Server starting: {server}")
        
        # Get user details
        user_info = await client.get_user("alice")
        print(f"User info: {user_info}")
        
    finally:
        await client.close()

# Run the example
asyncio.run(main())
```

### Group Management

```python
async def manage_groups():
    client = HubClient()
    
    try:
        # Create a group
        group = await client.create_group("data-scientists", ["alice", "bob"])
        
        # List all groups
        groups = await client.list_groups()
        
        # Add user to group
        await client.add_user_to_group("data-scientists", "charlie")
        
        # Remove user from group
        await client.remove_user_from_group("data-scientists", "bob")
        
    finally:
        await client.close()
```

### Server Management with Options

```python
async def manage_servers():
    client = HubClient()
    
    try:
        # Start server with custom options
        options = {
            "image": "jupyter/scipy-notebook:latest",
            "cpu_limit": 2.0,
            "mem_limit": "4G",
            "env": {
                "JUPYTER_ENABLE_LAB": "yes"
            }
        }
        
        server = await client.start_server("alice", options=options)
        
        # Check server status
        server_info = await client.get_server("alice")
        print(f"Server ready: {server_info['ready']}")
        
        # Stop server
        await client.stop_server("alice")
        
    finally:
        await client.close()
```

## API Examples

### Using curl

```bash
# Set your token
export TOKEN="your-admin-token"
export HUB_URL="https://your-hub.example.com"

# List users
curl -H "Authorization: token $TOKEN" \
     "$HUB_URL/hub/api/users"

# Create user
curl -X POST \
     -H "Authorization: token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "newuser", "admin": false}' \
     "$HUB_URL/hub/api/users"

# Start server
curl -X POST \
     -H "Authorization: token $TOKEN" \
     "$HUB_URL/hub/api/users/alice/servers/"

# Get server status
curl -H "Authorization: token $TOKEN" \
     "$HUB_URL/hub/api/users/alice/servers/"
```

### Using Python requests

```python
import requests

class JupyterHubAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        self.headers = {'Authorization': f'token {token}'}
    
    def list_users(self):
        response = requests.get(
            f"{self.base_url}/hub/api/users",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def create_user(self, username, admin=False):
        response = requests.post(
            f"{self.base_url}/hub/api/users",
            headers=self.headers,
            json={"name": username, "admin": admin}
        )
        response.raise_for_status()
        return response.json()

# Usage
api = JupyterHubAPI("https://your-hub.example.com", "your-token")
users = api.list_users()
new_user = api.create_user("testuser")
```

## FastAPI Manager Examples

### Using the Manager API

```python
import httpx

async def use_manager_api():
    async with httpx.AsyncClient() as client:
        # List users through manager API
        response = await client.get("http://localhost:8080/users")
        users = response.json()
        
        # Create user
        response = await client.post(
            "http://localhost:8080/users",
            json={"name": "newuser", "admin": False}
        )
        
        # Start server
        response = await client.post(
            "http://localhost:8080/users/newuser/servers/"
        )
```

## Streamlit UI Usage

### Running the UI

```bash
# Set environment variables
export JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
export JUPYTERHUB_MANAGER_API_TOKEN=your-admin-token

# Run Streamlit app
streamlit run jupyterhub_manager/ui/app.py
```

### UI Features

1. **Dashboard**: Overview of hub status and metrics
2. **Users**: Create, delete, and manage users
3. **Groups**: Manage user groups
4. **Servers**: Start/stop servers, view status
5. **Services**: Monitor hub services
6. **Tokens**: Create and manage API tokens
7. **Admin**: Administrative operations

## Bulk Operations

### Bulk User Creation

```python
async def create_multiple_users():
    client = HubClient()
    
    try:
        usernames = ["student1", "student2", "student3", "instructor1"]
        
        for username in usernames:
            admin = username.startswith("instructor")
            user = await client.create_user(username, admin=admin)
            print(f"Created {username} (admin: {admin})")
            
        # Add students to group
        await client.create_group("students", 
                                 [u for u in usernames if u.startswith("student")])
        
    finally:
        await client.close()
```

### Bulk Server Management

```python
async def start_all_user_servers():
    client = HubClient()
    
    try:
        users = await client.list_users()
        
        for user in users:
            if not user.get("servers"):  # No running servers
                try:
                    await client.start_server(user["name"])
                    print(f"Started server for {user['name']}")
                except Exception as e:
                    print(f"Failed to start server for {user['name']}: {e}")
                    
    finally:
        await client.close()
```

## Error Handling

```python
import httpx
from jupyterhub_manager.client.base import HubClient

async def robust_operations():
    client = HubClient()
    
    try:
        # Handle user not found
        try:
            user = await client.get_user("nonexistent")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print("User not found")
            else:
                print(f"API error: {e}")
        
        # Handle server spawn failure
        try:
            server = await client.start_server("problematic-user")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                print("Server spawn failed")
            else:
                raise
                
    finally:
        await client.close()
```

## Monitoring and Health Checks

```python
async def health_monitor():
    client = HubClient()
    
    try:
        health = await client.get_health()
        
        if health["status"] == "ok":
            print("✅ Hub is healthy")
        else:
            print(f"❌ Hub health issue: {health.get('detail')}")
            
        # Check proxy status
        proxy = await client.get_proxy()
        print(f"Proxy routes: {len(proxy.get('routes', {}))}")
        
    finally:
        await client.close()
```
