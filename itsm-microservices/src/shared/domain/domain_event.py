from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from abc import ABC


@dataclass
class DomainEvent(ABC):
  event_id: str
  aggregate_id: str
  aggregate_type: str
  event_type: str
  timestamp: datetime = field(default_factory=datetime.utcnow)
  data: Dict[str, Any] = field(default_factory=dict)

  def to_dict(self) -> Dict[str, Any]:
    return {
      "event_id": self.event_id,
      "aggregate_id": self.aggregate_id,
      "aggregate_type": self.aggregate_type,
      "event_type": self.event_type,
      "timestamp": self.timestamp.isoformat(),
      "data": self.data,
    }


@dataclass
class IncidentCreated(DomainEvent):
  pass


@dataclass
class IncidentAssigned(DomainEvent):
  pass


@dataclass
class IncidentStatusChanged(DomainEvent):
  pass


@dataclass
class IncidentResolved(DomainEvent):
  pass


@dataclass
class IncidentClosed(DomainEvent):
  pass


@dataclass
class SLABreached(DomainEvent):
  pass


@dataclass
class SLAWarning(DomainEvent):
  pass
