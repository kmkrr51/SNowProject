from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CreateChangeCommand:
  title: str
  description: str
  change_type: str
  risk_level: str
  created_by: str


@dataclass
class SetImpactAssessmentCommand:
  change_id: str
  assessment: str


@dataclass
class SetRollbackPlanCommand:
  change_id: str
  plan: str


@dataclass
class SetImplementationScheduleCommand:
  change_id: str
  schedule: datetime


@dataclass
class SubmitForApprovalCommand:
  change_id: str


@dataclass
class ApproveChangeCommand:
  change_id: str
  approver_id: str
  comments: Optional[str] = None


@dataclass
class RejectChangeCommand:
  change_id: str
  approver_id: str
  reason: str


@dataclass
class ImplementChangeCommand:
  change_id: str


@dataclass
class RollbackChangeCommand:
  change_id: str
