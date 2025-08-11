# Architecture

The project is organized into logical components:

- `jupyterhub_manager/settings.py` Pydantic settings loaded from environment.
- `jupyterhub_manager/client` Async HTTP client wrapper for JupyterHub REST API.
- `jupyterhub_manager/api` FastAPI application exposing a simplified management API (with automatic OpenAPI / Swagger docs at `/docs`).
- `jupyterhub_manager/ui` Streamlit UI interacting directly with the Hub API client.
- `tests` pytest suite using `httpx.AsyncClient` to test FastAPI routes (with monkeypatching).
- `docker` Container build recipes for API and UI.
- `k8s` Example Kubernetes deployment & service manifests.

## Data Flow

User -> Streamlit UI -> HubClient -> JupyterHub REST
User -> FastAPI -> HubClient -> JupyterHub REST

## Extensibility

Add new JupyterHub endpoints by implementing methods on `HubClient` and corresponding FastAPI route functions.
