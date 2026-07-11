from dataclasses import dataclass
from typing import Optional
from ...shared.domain import Priority, ImpactLevel, UrgencyLevel


@dataclass
class CreateIncidentCommand:
  title: str
  description: str
  priority: str
  impact_level: str
  urgency_level: str
  created_by: str


@dataclass
class AssignIncidentCommand:
  incident_id: str
  technician_id: str


@dataclass
class ChangeIncidentStatusCommand:
  incident_id: str
  new_status: str


@dataclass
class ResolveIncidentCommand:
  incident_id: str


@dataclass
class CloseIncidentCommand:
  incident_id: str


@dataclass
class UpdateIncidentCommand:
  incident_id: str
  title: Optional[str] = None
  description: Optional[str] = None
  priority: Optional[str] = None
