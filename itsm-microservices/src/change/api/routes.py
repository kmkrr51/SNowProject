from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
  CreateChangeRequest,
  SetImpactAssessmentRequest,
  SetRollbackPlanRequest,
  SetImplementationScheduleRequest,
  ApproveChangeRequest,
  RejectChangeRequest,
  ChangeResponse,
  ChangeListResponse,
  ApprovalInfo,
  ErrorResponse,
)
from ..application.commands import (
  CreateChangeCommand,
  SetImpactAssessmentCommand,
  SetRollbackPlanCommand,
  SetImplementationScheduleCommand,
  SubmitForApprovalCommand,
  ApproveChangeCommand,
  RejectChangeCommand,
  ImplementChangeCommand,
  RollbackChangeCommand,
)
from ..application.queries import ListChangesQuery, GetChangeQuery
from ..infrastructure.repositories import ChangeRequestRepository
from ..application.handlers import (
  CreateChangeHandler,
  SetImpactAssessmentHandler,
  SetRollbackPlanHandler,
  SetImplementationScheduleHandler,
  SubmitForApprovalHandler,
  ApproveChangeHandler,
  RejectChangeHandler,
  ImplementChangeHandler,
  RollbackChangeHandler,
  GetChangeQueryHandler,
  ListChangesQueryHandler,
)

router = APIRouter(prefix="/api/v1/changes", tags=["changes"])


async def get_session():
  from ...shared.infrastructure import get_database_engine, get_session_factory
  engine = await get_database_engine()
  factory = await get_session_factory(engine)
  async with factory() as session:
    yield session


@router.post("", response_model=dict, status_code=201)
async def create_change(
  request: CreateChangeRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = CreateChangeHandler(repository)

    command = CreateChangeCommand(
      title=request.title,
      description=request.description,
      change_type=request.change_type,
      risk_level=request.risk_level,
      created_by=request.created_by,
    )

    change_id = await handler.handle(command)
    await session.commit()

    return {"id": change_id, "message": "Change created successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/{change_id}", response_model=ChangeResponse)
async def get_change(
  change_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = GetChangeQueryHandler(repository)

    query = GetChangeQuery(change_id=change_id)
    change = await handler.handle(query)

    if not change:
      raise HTTPException(status_code=404, detail=f"Change {change_id} not found")

    approvals = [
      ApprovalInfo(
        approver_id=a["approver_id"],
        status=a["status"],
        comments=a.get("comments"),
        approved_at=a.get("approved_at", ""),
      )
      for a in change.approvals
    ]

    return ChangeResponse(
      id=change.change_id,
      title=change.title.value,
      description=change.description.value,
      change_type=change.change_type,
      status=change.status,
      risk_level=change.risk_level,
      impact_assessment=change.impact_assessment,
      rollback_plan=change.rollback_plan,
      implementation_schedule=change.implementation_schedule,
      created_by=str(change.created_by),
      created_at=change.created_at.value,
      updated_at=change.updated_at.value,
      implemented_at=change.implemented_at,
      rolled_back_at=change.rolled_back_at,
      approvals=approvals,
    )
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ChangeListResponse)
async def list_changes(
  status: Optional[str] = Query(None),
  risk_level: Optional[str] = Query(None),
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = ListChangesQueryHandler(repository)

    query = ListChangesQuery(
      status=status,
      risk_level=risk_level,
      limit=limit,
      offset=offset,
    )
    result = await handler.handle(query)

    changes = [
      ChangeResponse(
        id=change.change_id,
        title=change.title.value,
        description=change.description.value,
        change_type=change.change_type,
        status=change.status,
        risk_level=change.risk_level,
        impact_assessment=change.impact_assessment,
        rollback_plan=change.rollback_plan,
        implementation_schedule=change.implementation_schedule,
        created_by=str(change.created_by),
        created_at=change.created_at.value,
        updated_at=change.updated_at.value,
        implemented_at=change.implemented_at,
        rolled_back_at=change.rolled_back_at,
        approvals=[
          ApprovalInfo(
            approver_id=a["approver_id"],
            status=a["status"],
            comments=a.get("comments"),
            approved_at=a.get("approved_at", ""),
          )
          for a in change.approvals
        ],
      )
      for change in result.get("changes", [])
    ]

    return ChangeListResponse(
      changes=changes,
      total=result.get("total", 0),
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/impact-assessment", status_code=200)
async def set_impact_assessment(
  change_id: str,
  request: SetImpactAssessmentRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = SetImpactAssessmentHandler(repository)

    command = SetImpactAssessmentCommand(
      change_id=change_id,
      assessment=request.assessment,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Impact assessment set successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/rollback-plan", status_code=200)
async def set_rollback_plan(
  change_id: str,
  request: SetRollbackPlanRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = SetRollbackPlanHandler(repository)

    command = SetRollbackPlanCommand(
      change_id=change_id,
      plan=request.plan,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Rollback plan set successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/submit", status_code=200)
async def submit_for_approval(
  change_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = SubmitForApprovalHandler(repository)

    command = SubmitForApprovalCommand(change_id=change_id)
    await handler.handle(command)
    await session.commit()

    return {"message": "Change submitted for approval successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/approve", status_code=200)
async def approve_change(
  change_id: str,
  request: ApproveChangeRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = ApproveChangeHandler(repository)

    command = ApproveChangeCommand(
      change_id=change_id,
      approver_id=request.approver_id,
      comments=request.comments,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Change approved successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/reject", status_code=200)
async def reject_change(
  change_id: str,
  request: RejectChangeRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = RejectChangeHandler(repository)

    command = RejectChangeCommand(
      change_id=change_id,
      approver_id=request.approver_id,
      reason=request.reason,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Change rejected successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/implement", status_code=200)
async def implement_change(
  change_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = ImplementChangeHandler(repository)

    command = ImplementChangeCommand(change_id=change_id)
    await handler.handle(command)
    await session.commit()

    return {"message": "Change implemented successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{change_id}/rollback", status_code=200)
async def rollback_change(
  change_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ChangeRequestRepository(session)
    handler = RollbackChangeHandler(repository)

    command = RollbackChangeCommand(change_id=change_id)
    await handler.handle(command)
    await session.commit()

    return {"message": "Change rolled back successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
