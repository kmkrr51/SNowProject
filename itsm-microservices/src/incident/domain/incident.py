from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from ...shared.domain import (
  AggregateRoot,
  IncidentId,
  Title,
  Description,
  Priority,
  Status,
  ImpactLevel,
  UrgencyLevel,
  TechnicianId,
  UserId,
  CreatedAt,
  UpdatedAt,
  SLAInfo,
  DomainEvent,
)
from .events import IncidentCreated, IncidentAssigned, IncidentStatusChanged


@dataclass
class Incident(AggregateRoot):
  incident_id: IncidentId
  title: Title
  description: Description
  priority: Priority
  status: Status
  impact_level: ImpactLevel
  urgency_level: UrgencyLevel
  assigned_to: Optional[TechnicianId] = None
  created_by: Optional[UserId] = None
  created_at: Optional[CreatedAt] = None
  updated_at: Optional[UpdatedAt] = None
  resolved_at: Optional[datetime] = None
  closed_at: Optional[datetime] = None
  sla_info: Optional[SLAInfo] = None

  def __init__(
    self,
    incident_id: IncidentId,
    title: Title,
    description: Description,
    priority: Priority,
    impact_level: ImpactLevel,
    urgency_level: UrgencyLevel,
    created_by: UserId,
  ):
    super().__init__(str(incident_id))
    self.incident_id = incident_id
    self.title = title
    self.description = description
    self.priority = priority
    self.status = Status.NEW
    self.impact_level = impact_level
    self.urgency_level = urgency_level
    self.created_by = created_by
    self.created_at = CreatedAt(datetime.utcnow())
    self.updated_at = UpdatedAt(datetime.utcnow())
    self.assigned_to = None
    self.resolved_at = None
    self.closed_at = None

    event = IncidentCreated(
      event_id=str(incident_id),
      aggregate_id=str(incident_id),
      aggregate_type="Incident",
      event_type="IncidentCreated",
      data={
        "incident_id": str(incident_id),
        "title": title.value,
        "priority": priority.value,
        "created_by": str(created_by),
      },
    )
    self.add_event(event)

  def assign_to(self, technician_id: TechnicianId) -> None:
    if self.assigned_to is not None:
      raise ValueError("Incident is already assigned")

    self.assigned_to = technician_id
    self.status = Status.ASSIGNED
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = IncidentAssigned(
      event_id=f"{self.incident_id}-assigned",
      aggregate_id=str(self.incident_id),
      aggregate_type="Incident",
      event_type="IncidentAssigned",
      data={
        "incident_id": str(self.incident_id),
        "assigned_to": str(technician_id),
      },
    )
    self.add_event(event)

  def change_status(self, new_status: Status) -> None:
    if self.status == new_status:
      raise ValueError(f"Incident is already in {new_status.value} status")

    old_status = self.status
    self.status = new_status
    self.updated_at = UpdatedAt(datetime.utcnow())

    if new_status == Status.RESOLVED:
      self.resolved_at = datetime.utcnow()
    elif new_status == Status.CLOSED:
      self.closed_at = datetime.utcnow()

    event = IncidentStatusChanged(
      event_id=f"{self.incident_id}-status-changed",
      aggregate_id=str(self.incident_id),
      aggregate_type="Incident",
      event_type="IncidentStatusChanged",
      data={
        "incident_id": str(self.incident_id),
        "old_status": old_status.value,
        "new_status": new_status.value,
      },
    )
    self.add_event(event)

  def is_assigned(self) -> bool:
    return self.assigned_to is not None

  def is_resolved(self) -> bool:
    return self.status == Status.RESOLVED

  def is_closed(self) -> bool:
    return self.status == Status.CLOSED
