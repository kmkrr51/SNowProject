from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ...shared.infrastructure import Base


class ProblemModel(Base):
  __tablename__ = "problems"

  id = Column(String(50), primary_key=True)
  title = Column(String(255), nullable=False)
  description = Column(String(2000), nullable=False)
  status = Column(String(50), nullable=False, default="NEW")
  root_cause = Column(Text, nullable=True)
  created_by = Column(String(50), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  resolved_at = Column(DateTime, nullable=True)
  related_incidents = Column(String(2000), nullable=True)
  impacted_services = Column(String(2000), nullable=True)

  rca_records = relationship("RCARecordModel", back_populates="problem", cascade="all, delete-orphan")
  known_errors = relationship("KnownErrorModel", back_populates="problem", cascade="all, delete-orphan")

  __table_args__ = (
    Index("idx_problems_status", "status"),
    Index("idx_problems_created_at", "created_at"),
  )


class RCARecordModel(Base):
  __tablename__ = "rca_records"

  id = Column(String(50), primary_key=True)
  problem_id = Column(String(50), ForeignKey("problems.id"), nullable=False)
  analysis_details = Column(Text, nullable=False)
  contributing_factors = Column(String(2000), nullable=True)
  timeline = Column(Text, nullable=True)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  problem = relationship("ProblemModel", back_populates="rca_records")


class KnownErrorModel(Base):
  __tablename__ = "known_errors"

  id = Column(String(50), primary_key=True)
  problem_id = Column(String(50), ForeignKey("problems.id"), nullable=False)
  workaround = Column(Text, nullable=False)
  temporary_fix = Column(Text, nullable=True)
  permanent_fix = Column(Text, nullable=True)
  status = Column(String(50), nullable=False, default="ACTIVE")
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  problem = relationship("ProblemModel", back_populates="known_errors")
