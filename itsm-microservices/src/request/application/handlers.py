from typing import Optional, List
from uuid import uuid4
from ...shared.domain import Title, Description, UserId
from ...shared.infrastructure import event_bus
from ..domain.service_request import ServiceRequest
from ..infrastructure.repositories import ServiceRequestRepository
from .commands import (
  CreateServiceRequestCommand,
  AssignServiceRequestCommand,
  AddTaskCommand,
  CompleteTaskCommand,
  FulfillServiceRequestCommand,
  CloseServiceRequestCommand,
)
from .queries import (
  GetServiceRequestQuery,
  ListServiceRequestsQuery,
  GetServiceRequestsByStatusQuery,
  GetServiceRequestsByRequesterQuery,
  GetServiceRequestsByAssignedToQuery,
)


class CreateServiceRequestHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, command: CreateServiceRequestCommand) -> str:
    request_id = f"REQ-{uuid4().hex[:8].upper()}"

    request = ServiceRequest(
      request_id=request_id,
      request_type=command.request_type,
      title=Title(command.title),
      description=Description(command.description),
      requester=UserId(command.requester),
      requested_service=command.requested_service,
      priority=command.priority,
    )

    await self.repository.save(request)

    for event in request.get_events():
      await event_bus.publish(event)

    request.clear_events()

    return request_id


class AssignServiceRequestHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, command: AssignServiceRequestCommand) -> None:
    request = await self.repository.get_by_id(command.request_id)
    if not request:
      raise ValueError(f"Service request {command.request_id} not found")

    request.assign_to(command.technician_id)
    await self.repository.save(request)

    for event in request.get_events():
      await event_bus.publish(event)

    request.clear_events()


class AddTaskHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, command: AddTaskCommand) -> None:
    request = await self.repository.get_by_id(command.request_id)
    if not request:
      raise ValueError(f"Service request {command.request_id} not found")

    request.add_task(command.task_name, command.description)
    await self.repository.save(request)


class CompleteTaskHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, command: CompleteTaskCommand) -> None:
    request = await self.repository.get_by_id(command.request_id)
    if not request:
      raise ValueError(f"Service request {command.request_id} not found")

    request.complete_task(command.task_index)
    await self.repository.save(request)


class FulfillServiceRequestHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, command: FulfillServiceRequestCommand) -> None:
    request = await self.repository.get_by_id(command.request_id)
    if not request:
      raise ValueError(f"Service request {command.request_id} not found")

    request.fulfill(command.fulfillment_details)
    await self.repository.save(request)

    for event in request.get_events():
      await event_bus.publish(event)

    request.clear_events()


class CloseServiceRequestHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, command: CloseServiceRequestCommand) -> None:
    request = await self.repository.get_by_id(command.request_id)
    if not request:
      raise ValueError(f"Service request {command.request_id} not found")

    request.close()
    await self.repository.save(request)

    for event in request.get_events():
      await event_bus.publish(event)

    request.clear_events()


class GetServiceRequestQueryHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, query: GetServiceRequestQuery) -> Optional[ServiceRequest]:
    return await self.repository.get_by_id(query.request_id)


class ListServiceRequestsQueryHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, query: ListServiceRequestsQuery) -> List[ServiceRequest]:
    requests = await self.repository.find_all()

    if query.status:
      requests = [r for r in requests if r.status == query.status]

    if query.priority:
      requests = [r for r in requests if r.priority == query.priority]

    if query.requester:
      requests = [r for r in requests if str(r.requester) == query.requester]

    if query.assigned_to:
      requests = [r for r in requests if r.assigned_to == query.assigned_to]

    requests = requests[query.offset : query.offset + query.limit]

    return requests


class GetServiceRequestsByStatusQueryHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, query: GetServiceRequestsByStatusQuery) -> List[ServiceRequest]:
    return await self.repository.find_by_status(query.status)


class GetServiceRequestsByRequesterQueryHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, query: GetServiceRequestsByRequesterQuery) -> List[ServiceRequest]:
    return await self.repository.find_by_requester(query.requester_id)


class GetServiceRequestsByAssignedToQueryHandler:
  def __init__(self, repository: ServiceRequestRepository):
    self.repository = repository

  async def handle(self, query: GetServiceRequestsByAssignedToQuery) -> List[ServiceRequest]:
    return await self.repository.find_by_assigned_to(query.technician_id)
