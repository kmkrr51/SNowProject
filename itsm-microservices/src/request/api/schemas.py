from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CreateServiceRequestRequest(BaseModel):
  request_type: str = Field(..., description="STANDARD, EMERGENCY, NORMAL")
  title: str = Field(..., min_length=1, max_length=255)
  description: str = Field(..., min_length=1, max_length=2000)
  requester: str = Field(..., min_length=1)
  requested_service: str = Field(..., min_length=1)
  priority: str = Field(..., description="HIGH, MEDIUM, LOW")


class AssignServiceRequestRequest(BaseModel):
  technician_id: str = Field(..., min_length=1)


class AddTaskRequest(BaseModel):
  task_name: str = Field(..., min_length=1, max_length=255)
  description: str = Field(..., min_length=1, max_length=2000)


class CompleteTaskRequest(BaseModel):
  task_index: int = Field(..., ge=0)


class FulfillServiceRequestRequest(BaseModel):
  fulfillment_details: str = Field(..., min_length=1, max_length=2000)


class TaskInfo(BaseModel):
  name: str
  description: str
  status: str
  created_at: str
  completed_at: Optional[str] = None


class ServiceRequestResponse(BaseModel):
  id: str
  request_type: str
  title: str
  description: str
  status: str
  requester: str
  requested_service: str
  priority: str
  assigned_to: Optional[str] = None
  fulfillment_details: Optional[str] = None
  tasks: List[TaskInfo] = []
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  fulfilled_at: Optional[datetime] = None
  closed_at: Optional[datetime] = None
  progress: float = 0.0

  class Config:
    from_attributes = True
    json_encoders = {
      datetime: lambda v: v.isoformat() if v else None
    }


class ServiceRequestListResponse(BaseModel):
  requests: List[ServiceRequestResponse]
  total: int
  limit: int
  offset: int


class ErrorResponse(BaseModel):
  error: str
  detail: Optional[str] = None
  status_code: int
