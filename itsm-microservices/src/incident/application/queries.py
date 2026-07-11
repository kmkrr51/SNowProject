from dataclasses import dataclass
from typing import Optional


@dataclass
class GetIncidentQuery:
  incident_id: str


@dataclass
class ListIncidentsQuery:
  status: Optional[str] = None
  priority: Optional[str] = None
  assigned_to: Optional[str] = None
  limit: int = 100
  offset: int = 0


@dataclass
class GetIncidentsByStatusQuery:
  status: str


@dataclass
class GetIncidentsByTechnicianQuery:
  technician_id: str
