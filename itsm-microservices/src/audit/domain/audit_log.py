from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from ...shared.domain import AggregateRoot, CreatedAt


@dataclass
class AuditLog(AggregateRoot):
  log_id: str
  entity_id: str
  entity_type: str
  action: str
  actor_id: str
  changes: Dict[str, Any]
  created_at: CreatedAt

  def __init__(
    self,
    log_id: str,
    entity_id: str,
    entity_type: str,
    action: str,
    actor_id: str,
    changes: Dict[str, Any],
  ):
    super().__init__(log_id)
    self.log_id = log_id
    self.entity_id = entity_id
    self.entity_type = entity_type
    self.action = action
    self.actor_id = actor_id
    self.changes = changes
    self.created_at = CreatedAt(datetime.utcnow())
