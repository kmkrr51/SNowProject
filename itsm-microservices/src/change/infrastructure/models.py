from sqlalchemy import Column, String, DateTime, Text, Integer, Index
from datetime import datetime
from ...shared.infrastructure import Base


class ChangeRequestModel(Base):
  __tablename__ = "change_requests"

  id = Column(String(50), primary_key=True)
  title = Column(String(255), nullable=False)
  description = Column(String(2000), nullable=False)
  change_type = Column(String(50), nullable=False)
  status = Column(String(50), nullable=False, default="DRAFT")
  risk_level = Column(String(50), nullable=False)
  impact_assessment = Column(Text, nullable=True)
  rollback_plan = Column(Text, nullable=True)
  implementation_schedule = Column(DateTime, nullable=True)
  created_by = Column(String(50), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  implemented_at = Column(DateTime, nullable=True)
  rolled_back_at = Column(DateTime, nullable=True)
  approvals = Column(Text, nullable=True)

  __table_args__ = (
    Index("idx_changes_status", "status"),
    Index("idx_changes_risk_level", "risk_level"),
    Index("idx_changes_created_at", "created_at"),
  )
