from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import AuditLogResponse, AuditLogListResponse
from ..infrastructure.repositories import AuditLogRepository

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


async def get_session():
  from ...shared.infrastructure import get_database_engine, get_session_factory
  engine = await get_database_engine()
  factory = await get_session_factory(engine)
  async with factory() as session:
    yield session


@router.get("/entity/{entity_type}/{entity_id}", response_model=AuditLogListResponse)
async def get_entity_audit_logs(
  entity_type: str,
  entity_id: str,
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = AuditLogRepository(session)
    logs = await repository.find_by_entity(entity_id, entity_type)
    paginated = logs[offset : offset + limit]

    return AuditLogListResponse(
      logs=[
        AuditLogResponse(
          id=log.log_id,
          entity_id=log.entity_id,
          entity_type=log.entity_type,
          action=log.action,
          actor_id=log.actor_id,
          changes=log.changes,
          created_at=log.created_at.value,
        )
        for log in paginated
      ],
      total=len(logs),
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/actor/{actor_id}", response_model=AuditLogListResponse)
async def get_actor_audit_logs(
  actor_id: str,
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = AuditLogRepository(session)
    logs = await repository.find_by_actor(actor_id)
    paginated = logs[offset : offset + limit]

    return AuditLogListResponse(
      logs=[
        AuditLogResponse(
          id=log.log_id,
          entity_id=log.entity_id,
          entity_type=log.entity_type,
          action=log.action,
          actor_id=log.actor_id,
          changes=log.changes,
          created_at=log.created_at.value,
        )
        for log in paginated
      ],
      total=len(logs),
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
