from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from ...shared.domain import (
  AggregateRoot,
  Title,
  Description,
  UserId,
  CreatedAt,
  UpdatedAt,
  DomainEvent,
)
from .events import (
  ServiceRequestCreated,
  ServiceRequestAssigned,
  ServiceRequestFulfilled,
  ServiceRequestClosed,
)


@dataclass
class ServiceRequest(AggregateRoot):
  request_id: str
  request_type: str
  title: Title
  description: Description
  status: str
  requester: UserId
  requested_service: str
  priority: str
  created_at: CreatedAt
  updated_at: UpdatedAt
  assigned_to: Optional[str] = None
  fulfillment_details: Optional[str] = None
  fulfilled_at: Optional[datetime] = None
  closed_at: Optional[datetime] = None
  tasks: List[dict] = field(default_factory=list)

  def __init__(
    self,
    request_id: str,
    request_type: str,
    title: Title,
    description: Description,
    requester: UserId,
    requested_service: str,
    priority: str,
  ):
    super().__init__(request_id)
    self.request_id = request_id
    self.request_type = request_type
    self.title = title
    self.description = description
    self.status = "NEW"
    self.requester = requester
    self.requested_service = requested_service
    self.priority = priority
    self.created_at = CreatedAt(datetime.utcnow())
    self.updated_at = UpdatedAt(datetime.utcnow())
    self.assigned_to = None
    self.fulfillment_details = None
    self.fulfilled_at = None
    self.closed_at = None
    self.tasks = []

    event = ServiceRequestCreated(
      event_id=request_id,
      aggregate_id=request_id,
      aggregate_type="ServiceRequest",
      event_type="ServiceRequestCreated",
      data={
        "request_id": request_id,
        "title": title.value,
        "request_type": request_type,
        "requester": str(requester),
      },
    )
    self.add_event(event)

  def assign_to(self, technician_id: str) -> None:
    if self.assigned_to is not None:
      raise ValueError("Request is already assigned")

    self.assigned_to = technician_id
    self.status = "ASSIGNED"
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ServiceRequestAssigned(
      event_id=f"{self.request_id}-assigned",
      aggregate_id=self.request_id,
      aggregate_type="ServiceRequest",
      event_type="ServiceRequestAssigned",
      data={
        "request_id": self.request_id,
        "assigned_to": technician_id,
      },
    )
    self.add_event(event)

  def add_task(self, task_name: str, description: str) -> None:
    if not task_name or len(task_name.strip()) == 0:
      raise ValueError("Task name cannot be empty")

    task = {
      "name": task_name,
      "description": description,
      "status": "PENDING",
      "created_at": datetime.utcnow().isoformat(),
    }
    self.tasks.append(task)
    self.updated_at = UpdatedAt(datetime.utcnow())

  def complete_task(self, task_index: int) -> None:
    if task_index < 0 or task_index >= len(self.tasks):
      raise ValueError("Invalid task index")

    self.tasks[task_index]["status"] = "COMPLETED"
    self.tasks[task_index]["completed_at"] = datetime.utcnow().isoformat()
    self.updated_at = UpdatedAt(datetime.utcnow())

  def fulfill(self, fulfillment_details: str) -> None:
    if self.status == "FULFILLED":
      raise ValueError("Request is already fulfilled")
    if not fulfillment_details or len(fulfillment_details.strip()) == 0:
      raise ValueError("Fulfillment details cannot be empty")

    self.status = "FULFILLED"
    self.fulfillment_details = fulfillment_details
    self.fulfilled_at = datetime.utcnow()
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ServiceRequestFulfilled(
      event_id=f"{self.request_id}-fulfilled",
      aggregate_id=self.request_id,
      aggregate_type="ServiceRequest",
      event_type="ServiceRequestFulfilled",
      data={
        "request_id": self.request_id,
        "fulfillment_details": fulfillment_details,
      },
    )
    self.add_event(event)

  def close(self) -> None:
    if self.status == "CLOSED":
      raise ValueError("Request is already closed")

    self.status = "CLOSED"
    self.closed_at = datetime.utcnow()
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ServiceRequestClosed(
      event_id=f"{self.request_id}-closed",
      aggregate_id=self.request_id,
      aggregate_type="ServiceRequest",
      event_type="ServiceRequestClosed",
      data={"request_id": self.request_id},
    )
    self.add_event(event)

  def is_assigned(self) -> bool:
    return self.assigned_to is not None

  def is_fulfilled(self) -> bool:
    return self.status == "FULFILLED"

  def is_closed(self) -> bool:
    return self.status == "CLOSED"

  def get_progress(self) -> float:
    if not self.tasks:
      return 0.0
    completed = sum(1 for t in self.tasks if t["status"] == "COMPLETED")
    return (completed / len(self.tasks)) * 100
