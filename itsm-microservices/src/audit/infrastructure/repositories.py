from typing import Optional, List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...shared.domain import Repository, CreatedAt
from ..domain.audit_log import AuditLog
from .models import AuditLogModel


class AuditLogRepository(Repository[AuditLog]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, log: AuditLog) -> None:
    model = AuditLogModel(
      id=log.log_id,
      entity_id=log.entity_id,
      entity_type=log.entity_type,
      action=log.action,
      actor_id=log.actor_id,
      changes=json.dumps(log.changes),
      created_at=log.created_at.value,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, log_id: str) -> Optional[AuditLog]:
    stmt = select(AuditLogModel).where(AuditLogModel.id == log_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    return self._model_to_domain(model)

  async def delete(self, log_id: str) -> None:
    stmt = select(AuditLogModel).where(AuditLogModel.id == log_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[AuditLog]:
    stmt = select(AuditLogModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()
    return [self._model_to_domain(m) for m in models]

  async def find_by_entity(self, entity_id: str, entity_type: str) -> List[AuditLog]:
    stmt = select(AuditLogModel).where(
      (AuditLogModel.entity_id == entity_id) & (AuditLogModel.entity_type == entity_type)
    )
    result = await self.session.execute(stmt)
    models = result.scalars().all()
    return [self._model_to_domain(m) for m in models]

  async def find_by_actor(self, actor_id: str) -> List[AuditLog]:
    stmt = select(AuditLogModel).where(AuditLogModel.actor_id == actor_id)
    result = await self.session.execute(stmt)
    models = result.scalars().all()
    return [self._model_to_domain(m) for m in models]

  def _model_to_domain(self, model: AuditLogModel) -> AuditLog:
    log = AuditLog(
      log_id=model.id,
      entity_id=model.entity_id,
      entity_type=model.entity_type,
      action=model.action,
      actor_id=model.actor_id,
      changes=json.loads(model.changes),
    )
    log.created_at = CreatedAt(model.created_at)
    return log
