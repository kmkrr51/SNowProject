from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class SearchResultResponse(BaseModel):
  id: str
  entity_id: str
  entity_type: str
  title: str
  description: str
  metadata: Dict[str, Any]
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True


class SearchResponse(BaseModel):
  results: list[SearchResultResponse]
  total: int
  query: str
