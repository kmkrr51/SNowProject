from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from ...shared.domain import (
  AggregateRoot,
  Title,
  Description,
  Status,
  UserId,
  CreatedAt,
  UpdatedAt,
  DomainEvent,
)
from .events import ProblemIdentified, RCAStarted, RCACompleted, ProblemResolved


@dataclass
class Problem(AggregateRoot):
  problem_id: str
  title: Title
  description: Description
  status: Status
  created_by: UserId
  created_at: CreatedAt
  updated_at: UpdatedAt
  related_incidents: List[str] = field(default_factory=list)
  root_cause: Optional[str] = None
  impacted_services: List[str] = field(default_factory=list)
  resolved_at: Optional[datetime] = None

  def __init__(
    self,
    problem_id: str,
    title: Title,
    description: Description,
    created_by: UserId,
  ):
    super().__init__(problem_id)
    self.problem_id = problem_id
    self.title = title
    self.description = description
    self.status = Status.NEW
    self.created_by = created_by
    self.created_at = CreatedAt(datetime.utcnow())
    self.updated_at = UpdatedAt(datetime.utcnow())
    self.related_incidents = []
    self.root_cause = None
    self.impacted_services = []
    self.resolved_at = None

    event = ProblemIdentified(
      event_id=problem_id,
      aggregate_id=problem_id,
      aggregate_type="Problem",
      event_type="ProblemIdentified",
      data={
        "problem_id": problem_id,
        "title": title.value,
        "created_by": str(created_by),
      },
    )
    self.add_event(event)

  def add_related_incident(self, incident_id: str) -> None:
    if incident_id not in self.related_incidents:
      self.related_incidents.append(incident_id)
      self.updated_at = UpdatedAt(datetime.utcnow())

  def add_impacted_service(self, service_name: str) -> None:
    if service_name not in self.impacted_services:
      self.impacted_services.append(service_name)
      self.updated_at = UpdatedAt(datetime.utcnow())

  def start_rca(self) -> None:
    if self.status != Status.NEW:
      raise ValueError("Can only start RCA on new problems")

    self.status = Status.IN_PROGRESS
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = RCAStarted(
      event_id=f"{self.problem_id}-rca-started",
      aggregate_id=self.problem_id,
      aggregate_type="Problem",
      event_type="RCAStarted",
      data={"problem_id": self.problem_id},
    )
    self.add_event(event)

  def complete_rca(self, root_cause: str) -> None:
    if self.status != Status.IN_PROGRESS:
      raise ValueError("RCA must be in progress")
    if not root_cause or len(root_cause.strip()) == 0:
      raise ValueError("Root cause cannot be empty")

    self.root_cause = root_cause
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = RCACompleted(
      event_id=f"{self.problem_id}-rca-completed",
      aggregate_id=self.problem_id,
      aggregate_type="Problem",
      event_type="RCACompleted",
      data={
        "problem_id": self.problem_id,
        "root_cause": root_cause,
      },
    )
    self.add_event(event)

  def resolve(self) -> None:
    if self.status == Status.RESOLVED:
      raise ValueError("Problem is already resolved")

    self.status = Status.RESOLVED
    self.resolved_at = datetime.utcnow()
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ProblemResolved(
      event_id=f"{self.problem_id}-resolved",
      aggregate_id=self.problem_id,
      aggregate_type="Problem",
      event_type="ProblemResolved",
      data={"problem_id": self.problem_id},
    )
    self.add_event(event)

  def is_resolved(self) -> bool:
    return self.status == Status.RESOLVED

  def has_root_cause(self) -> bool:
    return self.root_cause is not None
