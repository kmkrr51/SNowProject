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
):
  try:
    mock_requests = [
      ServiceRequestResponse(
        id="REQ-001",
        request_type="HARDWARE",
        title="New Laptop Request",
        description="Request for new laptop for new team member",
        status="FULFILLED",
        requester="john.doe@company.com",
        requested_service="Hardware Procurement",
        priority="MEDIUM",
        assigned_to="it.support@company.com",
        fulfillment_details="Laptop delivered on 2024-07-10",
        tasks=[
          TaskInfo(
            name="Approve Request",
            description="Manager approval",
            status="COMPLETED",
            created_at="2024-07-08T10:00:00Z",
            completed_at="2024-07-08T11:00:00Z",
          ),
          TaskInfo(
            name="Procure Hardware",
            description="Order laptop from vendor",
            status="COMPLETED",
            created_at="2024-07-08T11:00:00Z",
            completed_at="2024-07-10T09:00:00Z",
          ),
        ],
        created_at="2024-07-08T10:00:00Z",
        updated_at="2024-07-10T14:00:00Z",
        fulfilled_at="2024-07-10T14:00:00Z",
        closed_at=None,
        progress=100,
      ),
      ServiceRequestResponse(
        id="REQ-002",
        request_type="SOFTWARE",
        title="License for Adobe Creative Suite",
        description="Request for Adobe Creative Suite license",
        status="IN_PROGRESS",
        requester="jane.smith@company.com",
        requested_service="Software Licensing",
        priority="HIGH",
        assigned_to="it.support@company.com",
        fulfillment_details="License procurement in progress",
        tasks=[
          TaskInfo(
            name="Approve Request",
            description="Manager approval",
            status="COMPLETED",
            created_at="2024-07-09T10:00:00Z",
            completed_at="2024-07-09T11:00:00Z",
          ),
          TaskInfo(
            name="Purchase License",
            description="Buy license from Adobe",
            status="IN_PROGRESS",
            created_at="2024-07-09T11:00:00Z",
            completed_at=None,
          ),
        ],
        created_at="2024-07-09T10:00:00Z",
        updated_at="2024-07-10T13:00:00Z",
        fulfilled_at=None,
        closed_at=None,
        progress=50,
      ),
    ]
    
    return ServiceRequestListResponse(
      requests=mock_requests[offset:offset+limit],
      total=len(mock_requests),
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
