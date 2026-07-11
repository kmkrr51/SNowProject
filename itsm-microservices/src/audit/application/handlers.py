from uuid import uuid4
from ...shared.domain.domain_event import DomainEvent
from ..domain.audit_log import AuditLog
from ..infrastructure.repositories import AuditLogRepository


class AuditEventHandler:
  def __init__(self, repository: AuditLogRepository):
    self.repository = repository

  async def handle_event(self, event: DomainEvent) -> None:
    log = AuditLog(
      log_id=f"AUDIT-{uuid4().hex[:8].upper()}",
      entity_id=event.aggregate_id,
      entity_type=event.aggregate_type,
      action=event.event_type,
      actor_id=event.data.get("created_by", event.data.get("approver_id", "SYSTEM")),
      changes=event.data,
    )
    await self.repository.save(log)
