import pytest
from httpx import AsyncClient
from jupyterhub_manager.api.main import app


@pytest.mark.asyncio
async def test_list_users(monkeypatch):
    from jupyterhub_manager.client.base import HubClient

    async def fake_list_users(self):  # type: ignore[override]
        return [{"name": "alice"}]

    monkeypatch.setattr(HubClient, "list_users", fake_list_users)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/users")
    assert r.status_code == 200
    assert r.json() == [{"name": "alice"}]
