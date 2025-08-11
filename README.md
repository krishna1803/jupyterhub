# 🚀 JupyterHub Manager

A professional, comprehensive Python module with FastAPI and Streamlit interfaces for managing JupyterHub instances via the official REST API.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)

## ✨ Features

- 🔧 **Comprehensive API Client**: Full async client for JupyterHub REST API
- 🚀 **FastAPI Service**: Professional REST API with automatic OpenAPI/Swagger documentation
- 🎨 **Streamlit Admin UI**: Modern, intuitive web interface
- 🐳 **Docker Support**: Production-ready containerized deployments
- ☸️ **Kubernetes Ready**: Complete manifests and Helm charts
- 🧪 **Fully Tested**: Comprehensive pytest suite with async support
- 📚 **Rich Documentation**: Detailed guides and examples
- 🔐 **Security First**: Token-based authentication and SSL support

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   FastAPI API   │    │   Python Client │
│                 │    │                 │    │                 │
│  Admin Portal   │    │  REST Endpoints │    │  Direct Access  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼───────────┐
                    │     HubClient           │
                    │   (Async HTTP Client)   │
                    └─────────────┬───────────┘
                                  │
                    ┌─────────────▼───────────┐
                    │     JupyterHub          │
                    │      REST API           │
                    └─────────────────────────┘
```

## 🚀 Quick Start

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd jupyterhub-manager

# Run the automated setup script
./setup-dev.sh

# Or manual setup:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
export JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
export JUPYTERHUB_MANAGER_API_TOKEN=your-admin-api-token

# Start the API server
uvicorn jupyterhub_manager.api.main:app --reload --host 0.0.0.0 --port 8080

# Start the UI (in another terminal)
streamlit run jupyterhub_manager/ui/app.py --server.port 8501
```

### Access the Services

- 📖 **API Documentation**: http://localhost:8080/docs
- 🎨 **Admin UI**: http://localhost:8501
- 📋 **Alternative API Docs**: http://localhost:8080/redoc

## 📦 Installation

### Using pip (when published)

```bash
pip install jupyterhub-manager
```

### From source

```bash
git clone <repository-url>
cd jupyterhub-manager
pip install -e .
```

## 🔧 Configuration

All configuration is handled via environment variables with the `JUPYTERHUB_MANAGER_` prefix:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JUPYTERHUB_URL` | ✅ | - | JupyterHub base URL |
| `API_TOKEN` | ✅ | - | Admin API token |
| `VERIFY_SSL` | ❌ | `true` | SSL certificate verification |
| `REQUEST_TIMEOUT` | ❌ | `30` | Request timeout in seconds |
| `API_HOST` | ❌ | `0.0.0.0` | FastAPI host |
| `API_PORT` | ❌ | `8080` | FastAPI port |

### Getting an Admin Token

1. Log into JupyterHub as an admin
2. Go to Control Panel → Token
3. Generate a new token
4. Set it as `JUPYTERHUB_MANAGER_API_TOKEN`

## 📖 Usage Examples

### Python Client

```python
import asyncio
from jupyterhub_manager.client.base import HubClient

async def main():
    client = HubClient()
    
    try:
        # List users
        users = await client.list_users()
        print(f"Found {len(users)} users")
        
        # Create user
        await client.create_user("alice", admin=False)
        
        # Start server
        await client.start_server("alice")
        
        # Manage groups
        await client.create_group("data-scientists", ["alice", "bob"])
        
    finally:
        await client.close()

asyncio.run(main())
```

### FastAPI Endpoints

The API provides comprehensive endpoints for:

- 👥 **User Management**: CRUD operations, admin privileges
- 🖥️ **Server Management**: Start/stop servers, custom configurations
- 👨‍👩‍👧‍👦 **Group Management**: Create groups, manage memberships
- 🔧 **Service Management**: Monitor and manage hub services
- 🔐 **Token Management**: Create and manage API tokens
- ⚙️ **Admin Operations**: Hub administration, maintenance

See [API Documentation](docs/api-reference.md) for complete endpoint reference.

### Streamlit UI Features

- 📊 **Dashboard**: Hub health, user metrics, activity charts
- 👥 **User Management**: Visual user creation, server controls
- 👨‍👩‍👧‍👦 **Group Management**: Interactive group administration
- 🖥️ **Server Monitoring**: Real-time server status and management
- 🔧 **Service Overview**: Service monitoring and status
- 🔐 **Token Management**: API token creation and management
- ⚙️ **Admin Panel**: Critical operations and maintenance

## 🐳 Docker Deployment

### Build Images

```bash
# API Service
docker build -f docker/Dockerfile.api -t jupyterhub-manager-api:latest .

# UI Service
docker build -f docker/Dockerfile.ui -t jupyterhub-manager-ui:latest .
```

### Run with Docker

```bash
# API
docker run -d \
  --name jhub-manager-api \
  -p 8080:8080 \
  -e JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com \
  -e JUPYTERHUB_MANAGER_API_TOKEN=your-token \
  jupyterhub-manager-api:latest

# UI
docker run -d \
  --name jhub-manager-ui \
  -p 8501:8501 \
  -e JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com \
  -e JUPYTERHUB_MANAGER_API_TOKEN=your-token \
  jupyterhub-manager-ui:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8080:8080"
    environment:
      - JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
      - JUPYTERHUB_MANAGER_API_TOKEN=your-token
  
  ui:
    build:
      context: .
      dockerfile: docker/Dockerfile.ui
    ports:
      - "8501:8501"
    environment:
      - JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
      - JUPYTERHUB_MANAGER_API_TOKEN=your-token
```

## ☸️ Kubernetes Deployment

### Using Manifests

```bash
# Create secret with API token
kubectl create secret generic jhub-admin-token --from-literal=token=your-token

# Update URLs in k8s/ manifests
# Apply manifests
kubectl apply -f k8s/
```

### Using Helm

```bash
# Install with Helm
helm install jupyterhub-manager ./helm \
  --set config.jupyterhubUrl=https://your-hub.example.com \
  --set secret.apiToken=your-token
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jupyterhub_manager --cov-report=html

# Run specific test categories
pytest tests/test_client.py -v
pytest tests/test_comprehensive.py -v
```

## 📚 Documentation

- [Configuration Guide](docs/configuration.md)
- [API Reference](docs/api-reference.md)
- [Usage Examples](docs/usage-examples.md)
- [Architecture Overview](docs/architecture.md)

## 🛠️ Development

### Setup Development Environment

```bash
# Use the setup script
./setup-dev.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Type checking
mypy jupyterhub_manager --ignore-missing-imports
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 API Coverage

Based on [JupyterHub REST API v5.2.1](https://jupyterhub.readthedocs.io/en/5.2.1/reference/rest-api.html):

- ✅ **Users**: List, get, create, delete, modify
- ✅ **Servers**: List, get, start, stop with options
- ✅ **Groups**: List, get, create, delete, manage members
- ✅ **Services**: List, get details
- ✅ **Tokens**: List, create, delete
- ✅ **Admin**: Health, info, proxy, shutdown, cull
- ✅ **Activity**: Track user activity
- 🔄 **OAuth**: Planned for future release

## 🔒 Security

- All API communication uses token-based authentication
- SSL/TLS verification enabled by default
- Environment-based configuration (no hardcoded secrets)
- Docker images run as non-root users
- Kubernetes RBAC support

## 📄 License

This project is licensed under the BSD-3-Clause License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [JupyterHub](https://github.com/jupyterhub/jupyterhub) team for the excellent REST API
- [FastAPI](https://fastapi.tiangolo.com/) for the modern web framework
- [Streamlit](https://streamlit.io/) for the intuitive UI framework

## 📞 Support

- 📚 [Documentation](docs/)
- 🐛 [Issue Tracker](../../issues)
- 💬 [Discussions](../../discussions)

---

**Made with ❤️ for the JupyterHub community**