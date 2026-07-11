from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ...shared.domain import AggregateRoot, CreatedAt


@dataclass
class Notification(AggregateRoot):
  notification_id: str
  recipient_id: str
  subject: str
  message: str
  notification_type: str
  related_entity_id: str
  related_entity_type: str
  status: str
  created_at: CreatedAt
  read_at: Optional[datetime] = None

  def __init__(
    self,
    notification_id: str,
    recipient_id: str,
    subject: str,
    message: str,
    notification_type: str,
    related_entity_id: str,
    related_entity_type: str,
  ):
    super().__init__(notification_id)
    self.notification_id = notification_id
    self.recipient_id = recipient_id
    self.subject = subject
    self.message = message
    self.notification_type = notification_type
    self.related_entity_id = related_entity_id
    self.related_entity_type = related_entity_type
    self.status = "UNREAD"
    self.created_at = CreatedAt(datetime.utcnow())
    self.read_at = None

  def mark_as_read(self) -> None:
    if self.status == "READ":
      raise ValueError("Notification is already read")
    self.status = "READ"
    self.read_at = datetime.utcnow()

  def is_read(self) -> bool:
    return self.status == "READ"
