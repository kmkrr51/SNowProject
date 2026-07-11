from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ...shared.infrastructure import Base
from ...shared.domain import Priority, Status, ImpactLevel, UrgencyLevel


class IncidentModel(Base):
  __tablename__ = "incidents"

  id = Column(String(50), primary_key=True)
  title = Column(String(255), nullable=False)
  description = Column(String(2000), nullable=False)
  priority = Column(SQLEnum(Priority), nullable=False)
  status = Column(SQLEnum(Status), nullable=False, default=Status.NEW)
  impact_level = Column(SQLEnum(ImpactLevel), nullable=False)
  urgency_level = Column(SQLEnum(UrgencyLevel), nullable=False)
  assigned_to = Column(String(50), ForeignKey("technicians.id"), nullable=True)
  created_by = Column(String(50), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  resolved_at = Column(DateTime, nullable=True)
  closed_at = Column(DateTime, nullable=True)

  work_notes = relationship("WorkNoteModel", back_populates="incident", cascade="all, delete-orphan")
  technician = relationship("TechnicianModel", back_populates="incidents")

  __table_args__ = (
    Index("idx_incidents_status", "status"),
    Index("idx_incidents_priority", "priority"),
    Index("idx_incidents_assigned_to", "assigned_to"),
    Index("idx_incidents_created_at", "created_at"),
  )


class TechnicianModel(Base):
  __tablename__ = "technicians"

  id = Column(String(50), primary_key=True)
  name = Column(String(255), nullable=False)
  skills = Column(String(1000), nullable=True)
  availability = Column(String(50), nullable=False, default="AVAILABLE")
  current_workload = Column(Integer, nullable=False, default=0)
  historical_resolution_rate = Column(Integer, nullable=False, default=0)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  incidents = relationship("IncidentModel", back_populates="technician")


class WorkNoteModel(Base):
  __tablename__ = "work_notes"

  id = Column(String(50), primary_key=True)
  incident_id = Column(String(50), ForeignKey("incidents.id"), nullable=False)
  technician_id = Column(String(50), ForeignKey("technicians.id"), nullable=False)
  content = Column(String(2000), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

  incident = relationship("IncidentModel", back_populates="work_notes")


class SLAModel(Base):
  __tablename__ = "slas"

  id = Column(String(50), primary_key=True)
  name = Column(String(255), nullable=False)
  priority = Column(SQLEnum(Priority), nullable=False)
  response_time_hours = Column(Integer, nullable=False)
  response_time_minutes = Column(Integer, nullable=False, default=0)
  resolution_time_hours = Column(Integer, nullable=False)
  resolution_time_minutes = Column(Integer, nullable=False, default=0)
  created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
  updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
