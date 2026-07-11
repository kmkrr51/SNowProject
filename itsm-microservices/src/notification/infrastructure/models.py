from sqlalchemy import Column, String, DateTime, Text, Index
from datetime import datetime
from ...shared.infrastructure import Base


class NotificationModel(Base):
  __tablename__ = "notifications"

  id = Column(String(50), primary_key=True)
  recipient_id = Column(String(50), nullable=False)
  subject = Column(String(255), nullable=False)
  message = Column(Text, nullable=False)
  notification_type = Column(String(50), nullable=False)
  related_entity_id = Column(String(50), nullable=False)
  related_entity_type = Column(String(50), nullable=False)
  status = Column(String(50), nullable=False, default="UNREAD")
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  read_at = Column(DateTime, nullable=True)

  __table_args__ = (
    Index("idx_notifications_recipient", "recipient_id"),
    Index("idx_notifications_status", "status"),
    Index("idx_notifications_created_at", "created_at"),
  )
