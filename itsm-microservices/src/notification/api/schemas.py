from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationResponse(BaseModel):
  id: str
  recipient_id: str
  subject: str
  message: str
  notification_type: str
  related_entity_id: str
  related_entity_type: str
  status: str
  created_at: datetime
  read_at: Optional[datetime] = None

  class Config:
    from_attributes = True


class NotificationListResponse(BaseModel):
  notifications: list[NotificationResponse]
  total: int
  unread_count: int
