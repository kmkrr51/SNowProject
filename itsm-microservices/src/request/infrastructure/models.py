from sqlalchemy import Column, String, DateTime, Text, Float, Index
from datetime import datetime
from ...shared.infrastructure import Base


class ServiceRequestModel(Base):
  __tablename__ = "service_requests"

  id = Column(String(50), primary_key=True)
  request_type = Column(String(50), nullable=False)
  title = Column(String(255), nullable=False)
  description = Column(String(2000), nullable=False)
  status = Column(String(50), nullable=False, default="NEW")
  requester = Column(String(50), nullable=False)
  requested_service = Column(String(255), nullable=False)
  priority = Column(String(50), nullable=False)
  assigned_to = Column(String(50), nullable=True)
  fulfillment_details = Column(Text, nullable=True)
  tasks = Column(Text, nullable=True)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  fulfilled_at = Column(DateTime, nullable=True)
  closed_at = Column(DateTime, nullable=True)

  __table_args__ = (
    Index("idx_requests_status", "status"),
    Index("idx_requests_priority", "priority"),
    Index("idx_requests_requester", "requester"),
    Index("idx_requests_created_at", "created_at"),
  )
