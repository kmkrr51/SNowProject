from sqlalchemy import Column, String, DateTime, Text, Index
from datetime import datetime
from ...shared.infrastructure import Base


class AuditLogModel(Base):
  __tablename__ = "audit_logs"

  id = Column(String(50), primary_key=True)
  entity_id = Column(String(50), nullable=False)
  entity_type = Column(String(50), nullable=False)
  action = Column(String(50), nullable=False)
  actor_id = Column(String(50), nullable=False)
  changes = Column(Text, nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

  __table_args__ = (
    Index("idx_audit_entity_type", "entity_type"),
    Index("idx_audit_actor_id", "actor_id"),
    Index("idx_audit_created_at", "created_at"),
  )
