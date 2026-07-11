from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from ...shared.domain import AggregateRoot, CreatedAt


@dataclass
class SearchIndex(AggregateRoot):
  index_id: str
  entity_id: str
  entity_type: str
  title: str
  description: str
  content: str
  metadata: Dict[str, Any]
  created_at: CreatedAt
  updated_at: datetime

  def __init__(
    self,
    index_id: str,
    entity_id: str,
    entity_type: str,
    title: str,
    description: str,
    content: str,
    metadata: Dict[str, Any],
  ):
    super().__init__(index_id)
    self.index_id = index_id
    self.entity_id = entity_id
    self.entity_type = entity_type
    self.title = title
    self.description = description
    self.content = content
    self.metadata = metadata
    self.created_at = CreatedAt(datetime.utcnow())
    self.updated_at = datetime.utcnow()

  def update_content(self, title: str, description: str, content: str) -> None:
    self.title = title
    self.description = description
    self.content = content
    self.updated_at = datetime.utcnow()
