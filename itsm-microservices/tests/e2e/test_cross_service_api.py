import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
class TestCrossServiceAPI:
  async def test_incident_to_problem_api_flow(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      incident_response = await client.post(
        "/api/v1/incidents",
        json={
          "title": "Recurring email issue",
          "description": "Email timeouts daily",
          "priority": "HIGH",
          "created_by": "user123",
        },
      )
      assert incident_response.status_code == 201
      incident_id = incident_response.json()["id"]

      problem_response = await client.post(
        "/api/v1/problems",
        json={
          "title": "Email service timeout",
          "description": "Root cause identified",
          "created_by": "user123",
        },
      )
      assert problem_response.status_code == 201
      problem_id = problem_response.json()["id"]

      add_incident_response = await client.post(
        f"/api/v1/problems/{problem_id}/related-incidents",
        json={"incident_id": incident_id},
      )
      assert add_incident_response.status_code == 200

      get_problem_response = await client.get(f"/api/v1/problems/{problem_id}")
      assert get_problem_response.status_code == 200
      problem_data = get_problem_response.json()
      assert incident_id in problem_data["related_incidents"]

  async def test_change_request_workflow_api(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      change_response = await client.post(
        "/api/v1/changes",
        json={
          "title": "Update email service",
          "description": "Upgrade to new version",
          "change_type": "STANDARD",
          "risk_level": "MEDIUM",
          "created_by": "user123",
        },
      )
      assert change_response.status_code == 201
      change_id = change_response.json()["id"]

      assessment_response = await client.post(
        f"/api/v1/changes/{change_id}/impact-assessment",
        json={"assessment": "Affects email service"},
      )
      assert assessment_response.status_code == 200

      rollback_response = await client.post(
        f"/api/v1/changes/{change_id}/rollback-plan",
        json={"plan": "Revert to previous version"},
      )
      assert rollback_response.status_code == 200

      submit_response = await client.post(
        f"/api/v1/changes/{change_id}/submit",
      )
      assert submit_response.status_code == 200

      approve_response = await client.post(
        f"/api/v1/changes/{change_id}/approve",
        json={"approver_id": "approver123"},
      )
      assert approve_response.status_code == 200

      get_response = await client.get(f"/api/v1/changes/{change_id}")
      assert get_response.status_code == 200
      change_data = get_response.json()
      assert change_data["status"] == "APPROVED"

  async def test_service_request_workflow_api(self):
    async with AsyncClient(app=app, base_url="http://test") as client:
      request_response = await client.post(
        "/api/v1/requests",
        json={
          "request_type": "STANDARD",
          "title": "Request for new laptop",
          "description": "Need a new laptop",
          "requester": "user123",
          "requested_service": "IT Hardware",
          "priority": "HIGH",
        },
      )
      assert request_response.status_code == 201
      request_id = request_response.json()["id"]

      assign_response = await client.post(
        f"/api/v1/requests/{request_id}/assign",
        json={"technician_id": "tech123"},
      )
      assert assign_response.status_code == 200

      task_response = await client.post(
        f"/api/v1/requests/{request_id}/tasks",
        json={
          "task_name": "Verify specifications",
          "description": "Check laptop specs",
        },
      )
      assert task_response.status_code == 201

      complete_response = await client.post(
        f"/api/v1/requests/{request_id}/tasks/0/complete",
      )
      assert complete_response.status_code == 200

      fulfill_response = await client.post(
        f"/api/v1/requests/{request_id}/fulfill",
        json={"fulfillment_details": "Laptop delivered"},
      )
      assert fulfill_response.status_code == 200

      get_response = await client.get(f"/api/v1/requests/{request_id}")
      assert get_response.status_code == 200
      request_data = get_response.json()
      assert request_data["status"] == "FULFILLED"
