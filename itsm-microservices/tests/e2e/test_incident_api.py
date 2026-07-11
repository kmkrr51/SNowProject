import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
class TestIncidentAPI:
  async def test_create_incident(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Email not working",
          "description": "Users cannot access email",
          "priority": "HIGH",
          "created_by": "user123",
        },
      )
      assert response.status_code == 201
      data = response.json()
      assert "id" in data
      assert data["message"] == "Incident created successfully"

  async def test_get_incident(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      create_response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Test incident",
          "description": "Test description",
          "priority": "MEDIUM",
          "created_by": "user123",
        },
      )
      incident_id = create_response.json()["id"]

      get_response = await client.get(f"/api/v1/incidents/{incident_id}")
      assert get_response.status_code == 200
      data = get_response.json()
      assert data["title"] == "Test incident"
      assert data["status"] == "NEW"

  async def test_list_incidents(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      response = await client.get("/api/v1/incidents")
      assert response.status_code == 200
      data = response.json()
      assert "incidents" in data
      assert "total" in data

  async def test_assign_incident(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      create_response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Assign test",
          "description": "Test assignment",
          "priority": "HIGH",
          "created_by": "user123",
        },
      )
      incident_id = create_response.json()["id"]

      assign_response = await client.post(
        f"/api/v1/incidents/{incident_id}/assign",
        json={"technician_id": "tech123"},
      )
      assert assign_response.status_code == 200

      get_response = await client.get(f"/api/v1/incidents/{incident_id}")
      data = get_response.json()
      assert data["assigned_to"] == "tech123"
      assert data["status"] == "ASSIGNED"

  async def test_change_incident_status(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      create_response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Status test",
          "description": "Test status change",
          "priority": "MEDIUM",
          "created_by": "user123",
        },
      )
      incident_id = create_response.json()["id"]

      status_response = await client.post(
        f"/api/v1/incidents/{incident_id}/change-status",
        json={"new_status": "IN_PROGRESS"},
      )
      assert status_response.status_code == 200

      get_response = await client.get(f"/api/v1/incidents/{incident_id}")
      data = get_response.json()
      assert data["status"] == "IN_PROGRESS"
