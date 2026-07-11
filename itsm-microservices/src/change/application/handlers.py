from typing import Optional, List
from uuid import uuid4
from ...shared.domain import Title, Description, UserId
from ...shared.infrastructure import event_bus
from ..domain.change_request import ChangeRequest
from ..infrastructure.repositories import ChangeRequestRepository
from .commands import (
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
from .queries import (
  GetChangeQuery,
  ListChangesQuery,
  GetChangesByStatusQuery,
  GetChangesByRiskLevelQuery,
)


class CreateChangeHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: CreateChangeCommand) -> str:
    change_id = f"CHG-{uuid4().hex[:8].upper()}"

    change = ChangeRequest(
      change_id=change_id,
      title=Title(command.title),
      description=Description(command.description),
      change_type=command.change_type,
      risk_level=command.risk_level,
      created_by=UserId(command.created_by),
    )

    await self.repository.save(change)

    for event in change.get_events():
      await event_bus.publish(event)

    change.clear_events()

    return change_id


class SetImpactAssessmentHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: SetImpactAssessmentCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.set_impact_assessment(command.assessment)
    await self.repository.save(change)


class SetRollbackPlanHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: SetRollbackPlanCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.set_rollback_plan(command.plan)
    await self.repository.save(change)


class SetImplementationScheduleHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: SetImplementationScheduleCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.set_implementation_schedule(command.schedule)
    await self.repository.save(change)


class SubmitForApprovalHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: SubmitForApprovalCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.submit_for_approval()
    await self.repository.save(change)

    for event in change.get_events():
      await event_bus.publish(event)

    change.clear_events()


class ApproveChangeHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: ApproveChangeCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.approve(command.approver_id, command.comments)
    await self.repository.save(change)

    for event in change.get_events():
      await event_bus.publish(event)

    change.clear_events()


class RejectChangeHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: RejectChangeCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.reject(command.approver_id, command.reason)
    await self.repository.save(change)

    for event in change.get_events():
      await event_bus.publish(event)

    change.clear_events()


class ImplementChangeHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: ImplementChangeCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.implement()
    await self.repository.save(change)

    for event in change.get_events():
      await event_bus.publish(event)

    change.clear_events()


class RollbackChangeHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, command: RollbackChangeCommand) -> None:
    change = await self.repository.get_by_id(command.change_id)
    if not change:
      raise ValueError(f"Change {command.change_id} not found")

    change.rollback()
    await self.repository.save(change)

    for event in change.get_events():
      await event_bus.publish(event)

    change.clear_events()


class GetChangeQueryHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, query: GetChangeQuery) -> Optional[ChangeRequest]:
    return await self.repository.get_by_id(query.change_id)


class ListChangesQueryHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, query: ListChangesQuery) -> List[ChangeRequest]:
    changes = await self.repository.find_all()

    if query.status:
      changes = [c for c in changes if c.status == query.status]

    if query.risk_level:
      changes = [c for c in changes if c.risk_level == query.risk_level]

    changes = changes[query.offset : query.offset + query.limit]

    return changes


class GetChangesByStatusQueryHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, query: GetChangesByStatusQuery) -> List[ChangeRequest]:
    return await self.repository.find_by_status(query.status)


class GetChangesByRiskLevelQueryHandler:
  def __init__(self, repository: ChangeRequestRepository):
    self.repository = repository

  async def handle(self, query: GetChangesByRiskLevelQuery) -> List[ChangeRequest]:
    return await self.repository.find_by_risk_level(query.risk_level)
