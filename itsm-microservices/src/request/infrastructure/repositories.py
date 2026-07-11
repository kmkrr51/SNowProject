from typing import Optional, List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...shared.domain import Repository, Title, Description, UserId, CreatedAt, UpdatedAt
from ..domain.service_request import ServiceRequest
from .models import ServiceRequestModel


class ServiceRequestRepository(Repository[ServiceRequest]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, request: ServiceRequest) -> None:
    model = ServiceRequestModel(
      id=request.request_id,
      request_type=request.request_type,
      title=request.title.value,
      description=request.description.value,
      status=request.status,
      requester=str(request.requester),
      requested_service=request.requested_service,
      priority=request.priority,
      assigned_to=request.assigned_to,
      fulfillment_details=request.fulfillment_details,
      tasks=json.dumps(request.tasks) if request.tasks else None,
      created_at=request.created_at.value,
      updated_at=request.updated_at.value,
      fulfilled_at=request.fulfilled_at,
      closed_at=request.closed_at,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, request_id: str) -> Optional[ServiceRequest]:
    stmt = select(ServiceRequestModel).where(ServiceRequestModel.id == request_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    req = ServiceRequest(
      request_id=model.id,
      request_type=model.request_type,
      title=Title(model.title),
      description=Description(model.description),
      requester=UserId(model.requester),
      requested_service=model.requested_service,
      priority=model.priority,
    )
    req.status = model.status
    req.assigned_to = model.assigned_to
    req.fulfillment_details = model.fulfillment_details
    req.created_at = CreatedAt(model.created_at)
    req.updated_at = UpdatedAt(model.updated_at)
    req.fulfilled_at = model.fulfilled_at
    req.closed_at = model.closed_at
    req.tasks = json.loads(model.tasks) if model.tasks else []

    return req

  async def delete(self, request_id: str) -> None:
    stmt = select(ServiceRequestModel).where(ServiceRequestModel.id == request_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[ServiceRequest]:
    stmt = select(ServiceRequestModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    requests = []
    for model in models:
      req = ServiceRequest(
        request_id=model.id,
        request_type=model.request_type,
        title=Title(model.title),
        description=Description(model.description),
        requester=UserId(model.requester),
        requested_service=model.requested_service,
        priority=model.priority,
      )
      req.status = model.status
      req.assigned_to = model.assigned_to
      req.fulfillment_details = model.fulfillment_details
      req.created_at = CreatedAt(model.created_at)
      req.updated_at = UpdatedAt(model.updated_at)
      req.fulfilled_at = model.fulfilled_at
      req.closed_at = model.closed_at
      req.tasks = json.loads(model.tasks) if model.tasks else []
      requests.append(req)

    return requests

  async def find_by_status(self, status: str) -> List[ServiceRequest]:
    stmt = select(ServiceRequestModel).where(ServiceRequestModel.status == status)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    requests = []
    for model in models:
      req = ServiceRequest(
        request_id=model.id,
        request_type=model.request_type,
        title=Title(model.title),
        description=Description(model.description),
        requester=UserId(model.requester),
        requested_service=model.requested_service,
        priority=model.priority,
      )
      req.status = model.status
      req.assigned_to = model.assigned_to
      req.fulfillment_details = model.fulfillment_details
      req.created_at = CreatedAt(model.created_at)
      req.updated_at = UpdatedAt(model.updated_at)
      req.fulfilled_at = model.fulfilled_at
      req.closed_at = model.closed_at
      req.tasks = json.loads(model.tasks) if model.tasks else []
      requests.append(req)

    return requests

  async def find_by_requester(self, requester_id: str) -> List[ServiceRequest]:
    stmt = select(ServiceRequestModel).where(ServiceRequestModel.requester == requester_id)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    requests = []
    for model in models:
      req = ServiceRequest(
        request_id=model.id,
        request_type=model.request_type,
        title=Title(model.title),
        description=Description(model.description),
        requester=UserId(model.requester),
        requested_service=model.requested_service,
        priority=model.priority,
      )
      req.status = model.status
      req.assigned_to = model.assigned_to
      req.fulfillment_details = model.fulfillment_details
      req.created_at = CreatedAt(model.created_at)
      req.updated_at = UpdatedAt(model.updated_at)
      req.fulfilled_at = model.fulfilled_at
      req.closed_at = model.closed_at
      req.tasks = json.loads(model.tasks) if model.tasks else []
      requests.append(req)

    return requests

  async def find_by_assigned_to(self, technician_id: str) -> List[ServiceRequest]:
    stmt = select(ServiceRequestModel).where(ServiceRequestModel.assigned_to == technician_id)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    requests = []
    for model in models:
      req = ServiceRequest(
        request_id=model.id,
        request_type=model.request_type,
        title=Title(model.title),
        description=Description(model.description),
        requester=UserId(model.requester),
        requested_service=model.requested_service,
        priority=model.priority,
      )
      req.status = model.status
      req.assigned_to = model.assigned_to
      req.fulfillment_details = model.fulfillment_details
      req.created_at = CreatedAt(model.created_at)
      req.updated_at = UpdatedAt(model.updated_at)
      req.fulfilled_at = model.fulfilled_at
      req.closed_at = model.closed_at
      req.tasks = json.loads(model.tasks) if model.tasks else []
      requests.append(req)

    return requests
