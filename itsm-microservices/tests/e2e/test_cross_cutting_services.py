import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
class TestCrossCuttingServices:
  async def test_notification_service_api(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      response = await client.get(
        "/api/v1/notifications/recipient/user123",
      )
      assert response.status_code == 200
      data = response.json()
      assert "notifications" in data
      assert "total" in data
      assert "unread_count" in data

  async def test_search_service_api(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      incident_response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Email not working",
          "description": "Users cannot access email",
          "priority": "HIGH",
          "created_by": "user123",
        },
      )
      assert incident_response.status_code == 201

      search_response = await client.get(
        "/api/v1/search?q=email&entity_type=INCIDENT",
      )
      assert search_response.status_code == 200
      data = search_response.json()
      assert "results" in data
      assert "total" in data
      assert "query" in data

  async def test_audit_service_api(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      incident_response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Test incident",
          "description": "Test description",
          "priority": "MEDIUM",
          "created_by": "user123",
        },
      )
      assert incident_response.status_code == 201
      incident_id = incident_response.json()["id"]

      audit_response = await client.get(
        f"/api/v1/audit/entity/INCIDENT/{incident_id}",
      )
      assert audit_response.status_code == 200
      data = audit_response.json()
      assert "logs" in data
      assert "total" in data

  async def test_audit_by_actor_api(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      response = await client.get(
        "/api/v1/audit/actor/user123",
      )
      assert response.status_code == 200
      data = response.json()
      assert "logs" in data
      assert "total" in data
