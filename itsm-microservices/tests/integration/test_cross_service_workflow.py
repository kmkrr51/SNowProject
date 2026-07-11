import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.domain import Title, Description, UserId
from src.incident.domain.incident import Incident
from src.problem.domain.problem import Problem
from src.change.domain.change_request import ChangeRequest
from src.request.domain.service_request import ServiceRequest
from src.incident.infrastructure.repositories import IncidentRepository
from src.problem.infrastructure.repositories import ProblemRepository
from src.change.infrastructure.repositories import ChangeRequestRepository
from src.request.infrastructure.repositories import ServiceRequestRepository


@pytest.mark.asyncio
class TestCrossServiceWorkflow:
  async def test_incident_to_problem_workflow(self, session: AsyncSession):
    incident_repo = IncidentRepository(session)
    problem_repo = ProblemRepository(session)

    incident = Incident(
      incident_id="INC-001",
      title=Title("Recurring email issue"),
      description=Description("Email timeouts happening daily"),
      priority="HIGH",
      created_by=UserId("user123"),
    )
    await incident_repo.save(incident)
    await session.commit()

    problem = Problem(
      problem_id="PROB-001",
      title=Title("Email service timeout"),
      description=Description("Root cause: connection pool exhaustion"),
      created_by=UserId("user123"),
    )
    problem.add_related_incident("INC-001")
    await problem_repo.save(problem)
    await session.commit()

    retrieved_problem = await problem_repo.get_by_id("PROB-001")
    assert "INC-001" in retrieved_problem.related_incidents

  async def test_change_to_request_workflow(self, session: AsyncSession):
    change_repo = ChangeRequestRepository(session)
    request_repo = ServiceRequestRepository(session)

    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update email service"),
      description=Description("Upgrade to new version"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )
    change.set_impact_assessment("Affects email service")
    change.set_rollback_plan("Revert to previous version")
    await change_repo.save(change)
    await session.commit()

    request = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Test email service"),
      description=Description("Verify email service works"),
      requester=UserId("user456"),
      requested_service="Email Service",
      priority="HIGH",
    )
    await request_repo.save(request)
    await session.commit()

    retrieved_change = await change_repo.get_by_id("CHG-001")
    retrieved_request = await request_repo.get_by_id("REQ-001")

    assert retrieved_change.title.value == "Update email service"
    assert retrieved_request.title.value == "Test email service"

  async def test_complete_incident_resolution_workflow(self, session: AsyncSession):
    incident_repo = IncidentRepository(session)
    problem_repo = ProblemRepository(session)
    change_repo = ChangeRequestRepository(session)

    incident = Incident(
      incident_id="INC-FULL-001",
      title=Title("Critical system issue"),
      description=Description("System performance degradation"),
      priority="CRITICAL",
      created_by=UserId("user123"),
    )
    incident.assign_to("tech123")
    await incident_repo.save(incident)
    await session.commit()

    problem = Problem(
      problem_id="PROB-FULL-001",
      title=Title("System performance issue"),
      description=Description("Identified root cause"),
      created_by=UserId("user123"),
    )
    problem.add_related_incident("INC-FULL-001")
    problem.start_rca()
    await problem_repo.save(problem)
    await session.commit()

    change = ChangeRequest(
      change_id="CHG-FULL-001",
      title=Title("Fix performance issue"),
      description=Description("Deploy performance patch"),
      change_type="STANDARD",
      risk_level="LOW",
      created_by=UserId("user123"),
    )
    change.set_impact_assessment("Low impact")
    change.set_rollback_plan("Quick rollback available")
    change.submit_for_approval()
    change.approve("approver123")
    await change_repo.save(change)
    await session.commit()

    retrieved_incident = await incident_repo.get_by_id("INC-FULL-001")
    retrieved_problem = await problem_repo.get_by_id("PROB-FULL-001")
    retrieved_change = await change_repo.get_by_id("CHG-FULL-001")

    assert retrieved_incident.assigned_to == "tech123"
    assert "INC-FULL-001" in retrieved_problem.related_incidents
    assert retrieved_change.is_approved()
