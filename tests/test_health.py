import pytest
from httpx import AsyncClient
from jupyterhub_manager.api.main import app


@pytest.mark.asyncio
async def test_health(monkeypatch):
    from jupyterhub_manager.client.base import HubClient

    async def fake_get_health(self):  # type: ignore[override]
        return {"status": "ok"}

    monkeypatch.setattr(HubClient, "get_health", fake_get_health)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
