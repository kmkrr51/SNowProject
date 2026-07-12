from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
  CreateServiceRequestRequest,
  AssignServiceRequestRequest,
  AddTaskRequest,
  CompleteTaskRequest,
  FulfillServiceRequestRequest,
  ServiceRequestResponse,
  ServiceRequestListResponse,
  TaskInfo,
  ErrorResponse,
)
from ..application.commands import (
  CreateServiceRequestCommand,
  AssignServiceRequestCommand,
  AddTaskCommand,
  CompleteTaskCommand,
  FulfillServiceRequestCommand,
  CloseServiceRequestCommand,
)
from ..application.queries import ListServiceRequestsQuery, GetServiceRequestQuery
from ..infrastructure.repositories import ServiceRequestRepository
from ..application.handlers import (
  CreateServiceRequestHandler,
  AssignServiceRequestHandler,
  AddTaskHandler,
  CompleteTaskHandler,
  FulfillServiceRequestHandler,
  CloseServiceRequestHandler,
  GetServiceRequestQueryHandler,
  ListServiceRequestsQueryHandler,
)

router = APIRouter(prefix="/api/v1/requests", tags=["requests"])


async def get_session():
  from ...shared.infrastructure import get_database_engine, get_session_factory
  engine = await get_database_engine()
  factory = await get_session_factory(engine)
  async with factory() as session:
    yield session


@router.post("", response_model=dict, status_code=201)
async def create_service_request(
  request: CreateServiceRequestRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = CreateServiceRequestHandler(repository)

    command = CreateServiceRequestCommand(
      request_type=request.request_type,
      title=request.title,
      description=request.description,
      requester=request.requester,
      requested_service=request.requested_service,
      priority=request.priority,
    )

    request_id = await handler.handle(command)
    await session.commit()

    return {"id": request_id, "message": "Service request created successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/{request_id}", response_model=ServiceRequestResponse)
async def get_service_request(
  request_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = GetServiceRequestQueryHandler(repository)

    query = GetServiceRequestQuery(request_id=request_id)
    req = await handler.handle(query)

    if not req:
      raise HTTPException(status_code=404, detail=f"Service request {request_id} not found")

    tasks = [
      TaskInfo(
        name=t["name"],
        description=t["description"],
        status=t["status"],
        created_at=t["created_at"],
        completed_at=t.get("completed_at"),
      )
      for t in req.tasks
    ]

    return ServiceRequestResponse(
      id=req.request_id,
      request_type=req.request_type,
      title=req.title.value,
      description=req.description.value,
      status=req.status,
      requester=str(req.requester),
      requested_service=req.requested_service,
      priority=req.priority,
      assigned_to=req.assigned_to,
      fulfillment_details=req.fulfillment_details,
      tasks=tasks,
      created_at=req.created_at.value,
      updated_at=req.updated_at.value,
      fulfilled_at=req.fulfilled_at,
      closed_at=req.closed_at,
      progress=req.get_progress(),
    )
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ServiceRequestListResponse)
async def list_service_requests(
  status: Optional[str] = Query(None),
  priority: Optional[str] = Query(None),
  requester: Optional[str] = Query(None),
  assigned_to: Optional[str] = Query(None),
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = ListServiceRequestsQueryHandler(repository)

    query = ListServiceRequestsQuery(
      status=status,
      priority=priority,
      requester=requester,
      assigned_to=assigned_to,
      limit=limit,
      offset=offset,
    )
    requests_list = await handler.handle(query)

    requests = [
      ServiceRequestResponse(
        id=req.request_id,
        request_type=req.request_type,
        title=req.title.value,
        description=req.description.value,
        status=req.status,
        requester=str(req.requester),
        requested_service=req.requested_service,
        priority=req.priority,
        assigned_to=req.assigned_to,
        fulfillment_details=req.fulfillment_details,
        tasks=[
          TaskInfo(
            name=t["name"],
            description=t["description"],
            status=t["status"],
            created_at=t["created_at"],
            completed_at=t.get("completed_at"),
          )
          for t in req.tasks
        ],
        created_at=req.created_at.value,
        updated_at=req.updated_at.value,
        fulfilled_at=req.fulfilled_at,
        closed_at=req.closed_at,
        progress=req.get_progress(),
      )
      for req in requests_list
    ]

    return ServiceRequestListResponse(
      requests=requests,
      total=len(requests_list),
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{request_id}/assign", status_code=200)
async def assign_service_request(
  request_id: str,
  request: AssignServiceRequestRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = AssignServiceRequestHandler(repository)

    command = AssignServiceRequestCommand(
      request_id=request_id,
      technician_id=request.technician_id,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Service request assigned successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{request_id}/tasks", status_code=201)
async def add_task(
  request_id: str,
  request: AddTaskRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = AddTaskHandler(repository)

    command = AddTaskCommand(
      request_id=request_id,
      task_name=request.task_name,
      description=request.description,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Task added successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{request_id}/tasks/{task_index}/complete", status_code=200)
async def complete_task(
  request_id: str,
  task_index: int,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = CompleteTaskHandler(repository)

    command = CompleteTaskCommand(
      request_id=request_id,
      task_index=task_index,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Task completed successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{request_id}/fulfill", status_code=200)
async def fulfill_service_request(
  request_id: str,
  request: FulfillServiceRequestRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = FulfillServiceRequestHandler(repository)

    command = FulfillServiceRequestCommand(
      request_id=request_id,
      fulfillment_details=request.fulfillment_details,
    )

    await handler.handle(command)
    await session.commit()

    return {"message": "Service request fulfilled successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{request_id}/close", status_code=200)
async def close_service_request(
  request_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ServiceRequestRepository(session)
    handler = CloseServiceRequestHandler(repository)

    command = CloseServiceRequestCommand(request_id=request_id)
    await handler.handle(command)
    await session.commit()

    return {"message": "Service request closed successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
