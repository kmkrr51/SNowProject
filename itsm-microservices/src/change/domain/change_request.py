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
  ChangeRequested,
  ChangeApprovalRequested,
  ChangeApproved,
  ChangeRejected,
  ChangeImplemented,
  ChangeRolledBack,
)


@dataclass
class ChangeRequest(AggregateRoot):
  change_id: str
  title: Title
  description: Description
  change_type: str
  status: str
  risk_level: str
  created_by: UserId
  created_at: CreatedAt
  updated_at: UpdatedAt
  impact_assessment: Optional[str] = None
  implementation_schedule: Optional[datetime] = None
  rollback_plan: Optional[str] = None
  approvals: List[dict] = field(default_factory=list)
  implemented_at: Optional[datetime] = None
  rolled_back_at: Optional[datetime] = None

  def __init__(
    self,
    change_id: str,
    title: Title,
    description: Description,
    change_type: str,
    risk_level: str,
    created_by: UserId,
  ):
    super().__init__(change_id)
    self.change_id = change_id
    self.title = title
    self.description = description
    self.change_type = change_type
    self.status = "DRAFT"
    self.risk_level = risk_level
    self.created_by = created_by
    self.created_at = CreatedAt(datetime.utcnow())
    self.updated_at = UpdatedAt(datetime.utcnow())
    self.impact_assessment = None
    self.implementation_schedule = None
    self.rollback_plan = None
    self.approvals = []
    self.implemented_at = None
    self.rolled_back_at = None

    event = ChangeRequested(
      event_id=change_id,
      aggregate_id=change_id,
      aggregate_type="ChangeRequest",
      event_type="ChangeRequested",
      data={
        "change_id": change_id,
        "title": title.value,
        "change_type": change_type,
        "created_by": str(created_by),
      },
    )
    self.add_event(event)

  def set_impact_assessment(self, assessment: str) -> None:
    if not assessment or len(assessment.strip()) == 0:
      raise ValueError("Impact assessment cannot be empty")
    self.impact_assessment = assessment
    self.updated_at = UpdatedAt(datetime.utcnow())

  def set_rollback_plan(self, plan: str) -> None:
    if not plan or len(plan.strip()) == 0:
      raise ValueError("Rollback plan cannot be empty")
    self.rollback_plan = plan
    self.updated_at = UpdatedAt(datetime.utcnow())

  def set_implementation_schedule(self, schedule: datetime) -> None:
    if schedule <= datetime.utcnow():
      raise ValueError("Implementation schedule must be in the future")
    self.implementation_schedule = schedule
    self.updated_at = UpdatedAt(datetime.utcnow())

  def submit_for_approval(self) -> None:
    if self.status != "DRAFT":
      raise ValueError("Only draft changes can be submitted for approval")
    if not self.impact_assessment:
      raise ValueError("Impact assessment required before approval")
    if not self.rollback_plan:
      raise ValueError("Rollback plan required before approval")

    self.status = "SUBMITTED"
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ChangeApprovalRequested(
      event_id=f"{self.change_id}-approval-requested",
      aggregate_id=self.change_id,
      aggregate_type="ChangeRequest",
      event_type="ChangeApprovalRequested",
      data={"change_id": self.change_id},
    )
    self.add_event(event)

  def approve(self, approver_id: str, comments: Optional[str] = None) -> None:
    if self.status not in ["SUBMITTED", "PENDING_APPROVAL"]:
      raise ValueError("Change must be submitted for approval")

    self.approvals.append({
      "approver_id": approver_id,
      "status": "APPROVED",
      "comments": comments,
      "approved_at": datetime.utcnow().isoformat(),
    })

    if self._all_approvals_received():
      self.status = "APPROVED"

    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ChangeApproved(
      event_id=f"{self.change_id}-approved",
      aggregate_id=self.change_id,
      aggregate_type="ChangeRequest",
      event_type="ChangeApproved",
      data={
        "change_id": self.change_id,
        "approver_id": approver_id,
      },
    )
    self.add_event(event)

  def reject(self, approver_id: str, reason: str) -> None:
    if self.status not in ["SUBMITTED", "PENDING_APPROVAL"]:
      raise ValueError("Change must be submitted for approval")
    if not reason or len(reason.strip()) == 0:
      raise ValueError("Rejection reason required")

    self.status = "REJECTED"
    self.approvals.append({
      "approver_id": approver_id,
      "status": "REJECTED",
      "comments": reason,
      "approved_at": datetime.utcnow().isoformat(),
    })
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ChangeRejected(
      event_id=f"{self.change_id}-rejected",
      aggregate_id=self.change_id,
      aggregate_type="ChangeRequest",
      event_type="ChangeRejected",
      data={
        "change_id": self.change_id,
        "approver_id": approver_id,
        "reason": reason,
      },
    )
    self.add_event(event)

  def implement(self) -> None:
    if self.status != "APPROVED":
      raise ValueError("Only approved changes can be implemented")

    self.status = "IMPLEMENTED"
    self.implemented_at = datetime.utcnow()
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ChangeImplemented(
      event_id=f"{self.change_id}-implemented",
      aggregate_id=self.change_id,
      aggregate_type="ChangeRequest",
      event_type="ChangeImplemented",
      data={"change_id": self.change_id},
    )
    self.add_event(event)

  def rollback(self) -> None:
    if self.status != "IMPLEMENTED":
      raise ValueError("Only implemented changes can be rolled back")

    self.status = "ROLLED_BACK"
    self.rolled_back_at = datetime.utcnow()
    self.updated_at = UpdatedAt(datetime.utcnow())

    event = ChangeRolledBack(
      event_id=f"{self.change_id}-rolled-back",
      aggregate_id=self.change_id,
      aggregate_type="ChangeRequest",
      event_type="ChangeRolledBack",
      data={"change_id": self.change_id},
    )
    self.add_event(event)

  def is_approved(self) -> bool:
    return self.status == "APPROVED"

  def is_implemented(self) -> bool:
    return self.status == "IMPLEMENTED"

  def is_rejected(self) -> bool:
    return self.status == "REJECTED"

  def _all_approvals_received(self) -> bool:
    return len(self.approvals) >= 1
