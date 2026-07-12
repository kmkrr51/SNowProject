from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
  CreateIncidentRequest,
  UpdateIncidentRequest,
  AssignIncidentRequest,
  ChangeStatusRequest,
  IncidentResponse,
  IncidentListResponse,
  ErrorResponse,
)
from .dependencies import (
  get_session,
  get_incident_repository,
  get_create_incident_handler,
  get_assign_incident_handler,
  get_change_status_handler,
  get_resolve_handler,
  get_close_handler,
  get_get_incident_handler,
  get_list_incidents_handler,
)
from ..application.commands import (
  CreateIncidentCommand,
  AssignIncidentCommand,
  ChangeIncidentStatusCommand,
  ResolveIncidentCommand,
  CloseIncidentCommand,
)
from ..application.queries import ListIncidentsQuery, GetIncidentQuery

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])


@router.post("", response_model=dict, status_code=201)
async def create_incident(
  request: CreateIncidentRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_create_incident_handler(repository)

    command = CreateIncidentCommand(
      title=request.title,
      description=request.description,
      priority=request.priority,
      impact_level=request.impact_level,
      urgency_level=request.urgency_level,
      created_by=request.created_by,
    )

    incident_id = await handler.handle(command)
    await session.commit()

    return {"id": incident_id, "message": "Incident created successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
  incident_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_get_incident_handler(repository)

    query = GetIncidentQuery(incident_id=incident_id)
    incident = await handler.handle(query)

    if not incident:
      raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    return IncidentResponse(
      id=str(incident.incident_id),
      title=incident.title.value,
      description=incident.description.value,
      priority=incident.priority.value,
      status=incident.status.value,
      impact_level=incident.impact_level.value,
      urgency_level=incident.urgency_level.value,
      assigned_to=str(incident.assigned_to) if incident.assigned_to else None,
      created_by=str(incident.created_by),
      created_at=incident.created_at.value,
      updated_at=incident.updated_at.value,
      resolved_at=incident.resolved_at,
      closed_at=incident.closed_at,
    )
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=IncidentListResponse)
async def list_incidents(
  status: Optional[str] = Query(None),
  priority: Optional[str] = Query(None),
  assigned_to: Optional[str] = Query(None),
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_list_incidents_handler(repository)

    query = ListIncidentsQuery(
      status=status,
      priority=priority,
      assigned_to=assigned_to,
      limit=limit,
      offset=offset,
    )
    incidents_list = await handler.handle(query)

    incidents = [
      IncidentResponse(
        id=str(incident.incident_id),
        title=incident.title.value,
        description=incident.description.value,
        priority=incident.priority.value,
        status=incident.status.value,
        impact_level=incident.impact_level.value,
        urgency_level=incident.urgency_level.value,
        assigned_to=str(incident.assigned_to) if incident.assigned_to else None,
        created_by=str(incident.created_by),
        created_at=incident.created_at.value,
        updated_at=incident.updated_at.value,
        resolved_at=incident.resolved_at,
        closed_at=incident.closed_at,
      )
      for incident in incidents_list
    ]

    return IncidentListResponse(
      incidents=incidents,
      total=len(incidents_list),
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{incident_id}/assign", status_code=200)
async def assign_incident(
  incident_id: str,
  request: AssignIncidentRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_assign_incident_handler(repository)

    command = AssignIncidentCommand(
      incident_id=incident_id,
      technician_id=request.technician_id,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Incident assigned successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{incident_id}/status", status_code=200)
async def change_incident_status(
  incident_id: str,
  request: ChangeStatusRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_change_status_handler(repository)

    command = ChangeIncidentStatusCommand(
      incident_id=incident_id,
      new_status=request.new_status,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Incident status changed successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{incident_id}/resolve", status_code=200)
async def resolve_incident(
  incident_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_resolve_handler(repository)

    command = ResolveIncidentCommand(incident_id=incident_id)

    await handler.handle(command)
    await session.commit()

    return {"message": "Incident resolved successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{incident_id}/close", status_code=200)
async def close_incident(
  incident_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = await get_incident_repository(session)
    handler = await get_close_handler(repository)

    command = CloseIncidentCommand(incident_id=incident_id)

    await handler.handle(command)
    await session.commit()

    return {"message": "Incident closed successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
