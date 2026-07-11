from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...shared.domain import Repository, IncidentId, TechnicianId, UserId
from ..domain.incident import Incident
from .models import IncidentModel, TechnicianModel


class IncidentRepository(Repository[Incident]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, incident: Incident) -> None:
    model = IncidentModel(
      id=str(incident.incident_id),
      title=incident.title.value,
      description=incident.description.value,
      priority=incident.priority,
      status=incident.status,
      impact_level=incident.impact_level,
      urgency_level=incident.urgency_level,
      assigned_to=str(incident.assigned_to) if incident.assigned_to else None,
      created_by=str(incident.created_by),
      created_at=incident.created_at.value if incident.created_at else None,
      updated_at=incident.updated_at.value if incident.updated_at else None,
      resolved_at=incident.resolved_at,
      closed_at=incident.closed_at,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, incident_id: str) -> Optional[Incident]:
    stmt = select(IncidentModel).where(IncidentModel.id == incident_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    from ...shared.domain import (
      Title,
      Description,
      CreatedAt,
      UpdatedAt,
    )

    incident = Incident(
      incident_id=IncidentId(model.id),
      title=Title(model.title),
      description=Description(model.description),
      priority=model.priority,
      impact_level=model.impact_level,
      urgency_level=model.urgency_level,
      created_by=UserId(model.created_by),
    )
    incident.status = model.status
    incident.assigned_to = TechnicianId(model.assigned_to) if model.assigned_to else None
    incident.created_at = CreatedAt(model.created_at)
    incident.updated_at = UpdatedAt(model.updated_at)
    incident.resolved_at = model.resolved_at
    incident.closed_at = model.closed_at

    return incident

  async def delete(self, incident_id: str) -> None:
    stmt = select(IncidentModel).where(IncidentModel.id == incident_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[Incident]:
    stmt = select(IncidentModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    from ...shared.domain import (
      Title,
      Description,
      CreatedAt,
      UpdatedAt,
    )

    incidents = []
    for model in models:
      incident = Incident(
        incident_id=IncidentId(model.id),
        title=Title(model.title),
        description=Description(model.description),
        priority=model.priority,
        impact_level=model.impact_level,
        urgency_level=model.urgency_level,
        created_by=UserId(model.created_by),
      )
      incident.status = model.status
      incident.assigned_to = TechnicianId(model.assigned_to) if model.assigned_to else None
      incident.created_at = CreatedAt(model.created_at)
      incident.updated_at = UpdatedAt(model.updated_at)
      incident.resolved_at = model.resolved_at
      incident.closed_at = model.closed_at
      incidents.append(incident)

    return incidents

  async def find_by_status(self, status: str) -> List[Incident]:
    from ...shared.domain import Status as StatusEnum, Title, Description, CreatedAt, UpdatedAt

    stmt = select(IncidentModel).where(IncidentModel.status == StatusEnum[status])
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    incidents = []
    for model in models:
      incident = Incident(
        incident_id=IncidentId(model.id),
        title=Title(model.title),
        description=Description(model.description),
        priority=model.priority,
        impact_level=model.impact_level,
        urgency_level=model.urgency_level,
        created_by=UserId(model.created_by),
      )
      incident.status = model.status
      incident.assigned_to = TechnicianId(model.assigned_to) if model.assigned_to else None
      incident.created_at = CreatedAt(model.created_at)
      incident.updated_at = UpdatedAt(model.updated_at)
      incident.resolved_at = model.resolved_at
      incident.closed_at = model.closed_at
      incidents.append(incident)

    return incidents

  async def find_by_assigned_to(self, technician_id: str) -> List[Incident]:
    from ...shared.domain import Title, Description, CreatedAt, UpdatedAt

    stmt = select(IncidentModel).where(IncidentModel.assigned_to == technician_id)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    incidents = []
    for model in models:
      incident = Incident(
        incident_id=IncidentId(model.id),
        title=Title(model.title),
        description=Description(model.description),
        priority=model.priority,
        impact_level=model.impact_level,
        urgency_level=model.urgency_level,
        created_by=UserId(model.created_by),
      )
      incident.status = model.status
      incident.assigned_to = TechnicianId(model.assigned_to) if model.assigned_to else None
      incident.created_at = CreatedAt(model.created_at)
      incident.updated_at = UpdatedAt(model.updated_at)
      incident.resolved_at = model.resolved_at
      incident.closed_at = model.closed_at
      incidents.append(incident)

    return incidents
