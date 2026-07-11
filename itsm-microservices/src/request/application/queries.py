from dataclasses import dataclass
from typing import Optional


@dataclass
class GetServiceRequestQuery:
  request_id: str


@dataclass
class ListServiceRequestsQuery:
  status: Optional[str] = None
  priority: Optional[str] = None
  requester: Optional[str] = None
  assigned_to: Optional[str] = None
  limit: int = 100
  offset: int = 0


@dataclass
class GetServiceRequestsByStatusQuery:
  status: str


@dataclass
class GetServiceRequestsByRequesterQuery:
  requester_id: str


@dataclass
class GetServiceRequestsByAssignedToQuery:
  technician_id: str
