# API Reference

## Overview

The JupyterHub Manager API provides a RESTful interface for managing JupyterHub instances. The API is built with FastAPI and provides automatic OpenAPI documentation.

## Authentication

All requests require a valid JupyterHub admin API token passed in the Authorization header:

```bash
Authorization: token your-admin-token
```

## Base URL

```
http://localhost:8080
```

## Endpoints

### Health & Info

#### GET /health
Get hub health status
```json
{
  "status": "ok",
  "version": "4.0.0"
}
```

#### GET /info  
Get hub information including version

### User Management

#### GET /users
List all users
```json
[
  {
    "name": "alice",
    "admin": false,
    "groups": ["scientists"],
    "servers": {}
  }
]
```

#### GET /users/{username}
Get specific user details

#### POST /users
Create a new user
```json
{
  "name": "newuser",
  "admin": false
}
```

#### DELETE /users/{username}
Delete a user

#### PATCH /users/{username}
Modify user properties
```json
{
  "admin": true
}
```

### Server Management

#### GET /users/{username}/servers
List user's servers

#### GET /users/{username}/servers/{server_name}
Get specific server details

#### POST /users/{username}/servers/{server_name}
Start a server for user
```json
{
  "image": "jupyter/scipy-notebook",
  "cpu_limit": 1.0,
  "mem_limit": "2G"
}
```

#### DELETE /users/{username}/servers/{server_name}
Stop a server for user

### Group Management

#### GET /groups
List all groups

#### GET /groups/{group_name}
Get specific group details

#### POST /groups
Create a new group
```json
{
  "name": "scientists",
  "users": ["alice", "bob"]
}
```

#### DELETE /groups/{group_name}
Delete a group

#### POST /groups/{group_name}/users
Add user to group

#### DELETE /groups/{group_name}/users/{username}
Remove user from group

### Service Management

#### GET /services
List all services

#### GET /services/{service_name}
Get specific service details

### Token Management

#### GET /tokens
List all tokens (admin only)

#### POST /users/{username}/tokens
Create API token for user
```json
{
  "note": "API access for data processing",
  "expires_in": 3600
}
```

#### DELETE /users/{username}/tokens/{token_id}
Delete a user's token

### Admin Operations

#### POST /admin/shutdown
Shutdown the hub (admin only)

#### GET /admin/proxy
Get proxy information

#### POST /admin/cull
Cull idle servers

## Error Responses

Standard HTTP status codes are used:

- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

Error response format:
```json
{
  "detail": "Error description"
}
```

## Rate Limiting

No rate limiting is currently implemented, but it's recommended to implement it in production environments.

## OpenAPI/Swagger

Interactive API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
