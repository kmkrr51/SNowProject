from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CreateChangeRequest(BaseModel):
  title: str = Field(..., min_length=1, max_length=255)
  description: str = Field(..., min_length=1, max_length=2000)
  change_type: str = Field(..., description="STANDARD, EMERGENCY, NORMAL")
  risk_level: str = Field(..., description="HIGH, MEDIUM, LOW")
  created_by: str = Field(..., min_length=1)


class SetImpactAssessmentRequest(BaseModel):
  assessment: str = Field(..., min_length=1, max_length=2000)


class SetRollbackPlanRequest(BaseModel):
  plan: str = Field(..., min_length=1, max_length=2000)


class SetImplementationScheduleRequest(BaseModel):
  schedule: datetime


class ApproveChangeRequest(BaseModel):
  approver_id: str = Field(..., min_length=1)
  comments: Optional[str] = None


class RejectChangeRequest(BaseModel):
  approver_id: str = Field(..., min_length=1)
  reason: str = Field(..., min_length=1, max_length=2000)


class ApprovalInfo(BaseModel):
  approver_id: str
  status: str
  comments: Optional[str] = None
  approved_at: str


class ChangeResponse(BaseModel):
  id: str
  title: str
  description: str
  change_type: str
  status: str
  risk_level: str
  impact_assessment: Optional[str] = None
  rollback_plan: Optional[str] = None
  implementation_schedule: Optional[datetime] = None
  created_by: str
  created_at: datetime
  updated_at: datetime
  implemented_at: Optional[datetime] = None
  rolled_back_at: Optional[datetime] = None
  approvals: List[ApprovalInfo] = []

  class Config:
    from_attributes = True


class ChangeListResponse(BaseModel):
  changes: List[ChangeResponse]
  total: int
  limit: int
  offset: int


class ErrorResponse(BaseModel):
  error: str
  detail: Optional[str] = None
  status_code: int
