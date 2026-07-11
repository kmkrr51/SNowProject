from dataclasses import dataclass
from datetime import datetime
from ...shared.domain import AggregateRoot, CreatedAt, UpdatedAt


@dataclass
class KnownError(AggregateRoot):
  known_error_id: str
  problem_id: str
  workaround: str
  temporary_fix: str
  permanent_fix: str
  status: str
  created_at: CreatedAt
  updated_at: UpdatedAt

  def __init__(
    self,
    known_error_id: str,
    problem_id: str,
    workaround: str,
    temporary_fix: str,
    permanent_fix: str,
  ):
    super().__init__(known_error_id)
    self.known_error_id = known_error_id
    self.problem_id = problem_id
    self.workaround = workaround
    self.temporary_fix = temporary_fix
    self.permanent_fix = permanent_fix
    self.status = "ACTIVE"
    self.created_at = CreatedAt(datetime.utcnow())
    self.updated_at = UpdatedAt(datetime.utcnow())

  def deactivate(self) -> None:
    self.status = "INACTIVE"
    self.updated_at = UpdatedAt(datetime.utcnow())

  def is_active(self) -> bool:
    return self.status == "ACTIVE"
