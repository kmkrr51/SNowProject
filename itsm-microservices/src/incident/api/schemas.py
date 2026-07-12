from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CreateIncidentRequest(BaseModel):
  model_config = ConfigDict(populate_by_name=True)

  title: str = Field(..., min_length=1, max_length=255)
  description: str = Field(..., min_length=1, max_length=2000)
  priority: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
  impact_level: str = Field(..., alias="impactLevel", description="HIGH, MEDIUM, LOW")
  urgency_level: str = Field(..., alias="urgencyLevel", description="HIGH, MEDIUM, LOW")
  created_by: str = Field(..., alias="createdBy", min_length=1)


class UpdateIncidentRequest(BaseModel):
  title: Optional[str] = Field(None, max_length=255)
  description: Optional[str] = Field(None, max_length=2000)
  priority: Optional[str] = None


class AssignIncidentRequest(BaseModel):
  technician_id: str = Field(..., min_length=1)


class ChangeStatusRequest(BaseModel):
  new_status: str = Field(..., description="NEW, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED")


class IncidentResponse(BaseModel):
  id: str
  title: str
  description: str
  priority: str
  status: str
  impact_level: str
  urgency_level: str
  assigned_to: Optional[str] = None
  created_by: str
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  resolved_at: Optional[datetime] = None
  closed_at: Optional[datetime] = None

  class Config:
    from_attributes = True
    json_encoders = {
      datetime: lambda v: v.isoformat() if v else None
    }


class IncidentListResponse(BaseModel):
  incidents: list[IncidentResponse]
  total: int
  limit: int
  offset: int


class ErrorResponse(BaseModel):
  error: str
  detail: Optional[str] = None
  status_code: int
