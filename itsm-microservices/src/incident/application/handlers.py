from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from ...shared.domain import (
  IncidentId,
  Title,
  Description,
  Priority,
  ImpactLevel,
  UrgencyLevel,
  TechnicianId,
  UserId,
  Status,
)
from ...shared.infrastructure import event_bus
from ..domain.incident import Incident
from ..infrastructure.repositories import IncidentRepository
from .commands import (
  CreateIncidentCommand,
  AssignIncidentCommand,
  ChangeIncidentStatusCommand,
  ResolveIncidentCommand,
  CloseIncidentCommand,
  UpdateIncidentCommand,
)
from .queries import (
  GetIncidentQuery,
  ListIncidentsQuery,
  GetIncidentsByStatusQuery,
  GetIncidentsByTechnicianQuery,
)


class CreateIncidentHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, command: CreateIncidentCommand) -> str:
    incident_id = IncidentId(f"INC-{uuid4().hex[:8].upper()}")

    incident = Incident(
      incident_id=incident_id,
      title=Title(command.title),
      description=Description(command.description),
      priority=Priority[command.priority],
      impact_level=ImpactLevel[command.impact_level],
      urgency_level=UrgencyLevel[command.urgency_level],
      created_by=UserId(command.created_by),
    )

    await self.repository.save(incident)

    for event in incident.get_events():
      await event_bus.publish(event)

    incident.clear_events()

    return str(incident_id)


class AssignIncidentHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, command: AssignIncidentCommand) -> None:
    incident = await self.repository.get_by_id(command.incident_id)
    if not incident:
      raise ValueError(f"Incident {command.incident_id} not found")

    incident.assign_to(TechnicianId(command.technician_id))
    await self.repository.save(incident)

    for event in incident.get_events():
      await event_bus.publish(event)

    incident.clear_events()


class ChangeIncidentStatusHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, command: ChangeIncidentStatusCommand) -> None:
    incident = await self.repository.get_by_id(command.incident_id)
    if not incident:
      raise ValueError(f"Incident {command.incident_id} not found")

    incident.change_status(Status[command.new_status])
    await self.repository.save(incident)

    for event in incident.get_events():
      await event_bus.publish(event)

    incident.clear_events()


class ResolveIncidentHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, command: ResolveIncidentCommand) -> None:
    incident = await self.repository.get_by_id(command.incident_id)
    if not incident:
      raise ValueError(f"Incident {command.incident_id} not found")

    incident.change_status(Status.RESOLVED)
    await self.repository.save(incident)

    for event in incident.get_events():
      await event_bus.publish(event)

    incident.clear_events()


class CloseIncidentHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, command: CloseIncidentCommand) -> None:
    incident = await self.repository.get_by_id(command.incident_id)
    if not incident:
      raise ValueError(f"Incident {command.incident_id} not found")

    incident.change_status(Status.CLOSED)
    await self.repository.save(incident)

    for event in incident.get_events():
      await event_bus.publish(event)

    incident.clear_events()


class GetIncidentQueryHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, query: GetIncidentQuery) -> Optional[Incident]:
    return await self.repository.get_by_id(query.incident_id)


class ListIncidentsQueryHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, query: ListIncidentsQuery) -> List[Incident]:
    incidents = await self.repository.find_all()

    if query.status:
      incidents = [i for i in incidents if i.status.value == query.status]

    if query.priority:
      incidents = [i for i in incidents if i.priority.value == query.priority]

    if query.assigned_to:
      incidents = [i for i in incidents if i.assigned_to and str(i.assigned_to) == query.assigned_to]

    incidents = incidents[query.offset : query.offset + query.limit]

    return incidents


class GetIncidentsByStatusQueryHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, query: GetIncidentsByStatusQuery) -> List[Incident]:
    return await self.repository.find_by_status(query.status)


class GetIncidentsByTechnicianQueryHandler:
  def __init__(self, repository: IncidentRepository):
    self.repository = repository

  async def handle(self, query: GetIncidentsByTechnicianQuery) -> List[Incident]:
    return await self.repository.find_by_assigned_to(query.technician_id)
