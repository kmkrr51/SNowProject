import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.domain import Title, Description, UserId
from src.incident.domain.incident import Incident
from src.incident.infrastructure.repositories import IncidentRepository


@pytest.mark.asyncio
class TestIncidentWorkflow:
  async def test_create_and_assign_incident(self, session: AsyncSession):
    repository = IncidentRepository(session)

    incident = Incident(
      incident_id="INC-001",
      title=Title("Email not working"),
      description=Description("Users cannot access email"),
      priority="HIGH",
      created_by=UserId("user123"),
    )

    await repository.save(incident)
    await session.commit()

    retrieved = await repository.get_by_id("INC-001")
    assert retrieved is not None
    assert retrieved.title.value == "Email not working"
    assert retrieved.status == "NEW"

    retrieved.assign_to("tech123")
    await repository.save(retrieved)
    await session.commit()

    updated = await repository.get_by_id("INC-001")
    assert updated.assigned_to == "tech123"
    assert updated.status == "ASSIGNED"

  async def test_incident_status_transitions(self, session: AsyncSession):
    repository = IncidentRepository(session)

    incident = Incident(
      incident_id="INC-002",
      title=Title("Database down"),
      description=Description("Database server is offline"),
      priority="CRITICAL",
      created_by=UserId("user456"),
    )

    await repository.save(incident)
    await session.commit()

    retrieved = await repository.get_by_id("INC-002")
    retrieved.assign_to("tech456")
    retrieved.change_status("IN_PROGRESS")
    await repository.save(retrieved)
    await session.commit()

    updated = await repository.get_by_id("INC-002")
    assert updated.status == "IN_PROGRESS"

    updated.resolve()
    await repository.save(updated)
    await session.commit()

    resolved = await repository.get_by_id("INC-002")
    assert resolved.is_resolved()

  async def test_list_incidents_by_status(self, session: AsyncSession):
    repository = IncidentRepository(session)

    for i in range(3):
      incident = Incident(
        incident_id=f"INC-{i}",
        title=Title(f"Issue {i}"),
        description=Description(f"Description {i}"),
        priority="HIGH",
        created_by=UserId("user123"),
      )
      await repository.save(incident)

    await session.commit()

    new_incidents = await repository.find_by_status("NEW")
    assert len(new_incidents) >= 3
