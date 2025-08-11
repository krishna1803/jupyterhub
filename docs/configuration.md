# Configuration Guide

## Environment Setup

The JupyterHub Manager uses environment variables for configuration. All variables are prefixed with `JUPYTERHUB_MANAGER_`.

### Required Variables

```bash
export JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
export JUPYTERHUB_MANAGER_API_TOKEN=your-admin-api-token
```

### Optional Variables

```bash
export JUPYTERHUB_MANAGER_VERIFY_SSL=true  # Default: true
export JUPYTERHUB_MANAGER_REQUEST_TIMEOUT=30  # Default: 30 seconds
export JUPYTERHUB_MANAGER_API_HOST=0.0.0.0  # Default: 0.0.0.0
export JUPYTERHUB_MANAGER_API_PORT=8080  # Default: 8080
```

## Getting an Admin API Token

1. Log into your JupyterHub as an admin user
2. Go to the admin panel
3. Navigate to "API Tokens"
4. Generate a new token with admin scope
5. Copy the token and set it as `JUPYTERHUB_MANAGER_API_TOKEN`

## Development Setup

```bash
# Clone and setup
git clone <repository>
cd jupyterhub-manager
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
export JUPYTERHUB_MANAGER_API_TOKEN=your-token

# Run API server
uvicorn jupyterhub_manager.api.main:app --reload --host 0.0.0.0 --port 8080

# Run UI (in another terminal)
streamlit run jupyterhub_manager/ui/app.py --server.port 8501
```

## Production Deployment

### Docker

```bash
# Build images
docker build -f docker/Dockerfile.api -t jupyterhub-manager-api:latest .
docker build -f docker/Dockerfile.ui -t jupyterhub-manager-ui:latest .

# Run with environment variables
docker run -d \
  --name jhub-manager-api \
  -p 8080:8080 \
  -e JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com \
  -e JUPYTERHUB_MANAGER_API_TOKEN=your-token \
  jupyterhub-manager-api:latest

docker run -d \
  --name jhub-manager-ui \
  -p 8501:8501 \
  -e JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com \
  -e JUPYTERHUB_MANAGER_API_TOKEN=your-token \
  jupyterhub-manager-ui:latest
```

### Kubernetes

1. Create a secret with your API token:
```bash
kubectl create secret generic jhub-admin-token --from-literal=token=your-token
```

2. Update the manifests in `k8s/` with your hub URL

3. Apply the manifests:
```bash
kubectl apply -f k8s/
```

## Security Considerations

- Always use HTTPS in production
- Rotate API tokens regularly
- Limit network access to the manager services
- Use proper RBAC in Kubernetes deployments
- Monitor access logs

## API Documentation

Once running, visit:
- API docs: `http://localhost:8080/docs`
- Alternative docs: `http://localhost:8080/redoc`
- UI: `http://localhost:8501`
