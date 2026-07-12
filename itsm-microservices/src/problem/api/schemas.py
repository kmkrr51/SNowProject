from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CreateProblemRequest(BaseModel):
  model_config = ConfigDict(populate_by_name=True)

  title: str = Field(..., min_length=1, max_length=255)
  description: str = Field(..., min_length=1, max_length=2000)
  created_by: str = Field(..., alias="createdBy", min_length=1)


class StartRCARequest(BaseModel):
  pass


class CompleteRCARequest(BaseModel):
  root_cause: str = Field(..., min_length=1, max_length=2000)


class AddRelatedIncidentRequest(BaseModel):
  incident_id: str = Field(..., min_length=1)


class AddImpactedServiceRequest(BaseModel):
  service_name: str = Field(..., min_length=1)


class CreateKnownErrorRequest(BaseModel):
  workaround: str = Field(..., min_length=1, max_length=2000)
  temporary_fix: str = Field(..., min_length=1, max_length=2000)
  permanent_fix: str = Field(..., min_length=1, max_length=2000)


class ProblemResponse(BaseModel):
  id: str
  title: str
  description: str
  status: str
  root_cause: Optional[str] = None
  created_by: str
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  resolved_at: Optional[datetime] = None
  related_incidents: List[str] = []
  impacted_services: List[str] = []

  class Config:
    from_attributes = True
    json_encoders = {
      datetime: lambda v: v.isoformat() if v else None
    }


class KnownErrorResponse(BaseModel):
  id: str
  problem_id: str
  workaround: str
  temporary_fix: str
  permanent_fix: str
  status: str
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  class Config:
    from_attributes = True
    json_encoders = {
      datetime: lambda v: v.isoformat() if v else None
    }


class ProblemListResponse(BaseModel):
  problems: List[ProblemResponse]
  total: int
  limit: int
  offset: int


class KnownErrorListResponse(BaseModel):
  known_errors: List[KnownErrorResponse]
  total: int
  limit: int
  offset: int


class ErrorResponse(BaseModel):
  error: str
  detail: Optional[str] = None
  status_code: int
