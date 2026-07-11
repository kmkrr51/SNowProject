from dataclasses import dataclass
from typing import Optional


@dataclass
class GetChangeQuery:
  change_id: str


@dataclass
class ListChangesQuery:
  status: Optional[str] = None
  risk_level: Optional[str] = None
  limit: int = 100
  offset: int = 0


@dataclass
class GetChangesByStatusQuery:
  status: str


@dataclass
class GetChangesByRiskLevelQuery:
  risk_level: str
