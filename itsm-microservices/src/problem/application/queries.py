from dataclasses import dataclass
from typing import Optional


@dataclass
class GetProblemQuery:
  problem_id: str


@dataclass
class ListProblemsQuery:
  status: Optional[str] = None
  limit: int = 100
  offset: int = 0


@dataclass
class GetProblemsByStatusQuery:
  status: str


@dataclass
class GetKnownErrorQuery:
  known_error_id: str


@dataclass
class ListKnownErrorsQuery:
  problem_id: Optional[str] = None
  limit: int = 100
  offset: int = 0


@dataclass
class GetKnownErrorsByProblemQuery:
  problem_id: str
