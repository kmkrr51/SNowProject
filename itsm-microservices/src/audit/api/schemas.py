from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class AuditLogResponse(BaseModel):
  id: str
  entity_id: str
  entity_type: str
  action: str
  actor_id: str
  changes: Dict[str, Any]
  created_at: datetime

  class Config:
    from_attributes = True


class AuditLogListResponse(BaseModel):
  logs: list[AuditLogResponse]
  total: int
