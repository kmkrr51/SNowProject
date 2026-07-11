from typing import Optional, List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...shared.domain import Repository, Title, Description, UserId, CreatedAt, UpdatedAt
from ..domain.change_request import ChangeRequest
from .models import ChangeRequestModel


class ChangeRequestRepository(Repository[ChangeRequest]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, change: ChangeRequest) -> None:
    model = ChangeRequestModel(
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
      approvals=json.dumps(change.approvals) if change.approvals else None,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, change_id: str) -> Optional[ChangeRequest]:
    stmt = select(ChangeRequestModel).where(ChangeRequestModel.id == change_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    change = ChangeRequest(
      change_id=model.id,
      title=Title(model.title),
      description=Description(model.description),
      change_type=model.change_type,
      risk_level=model.risk_level,
      created_by=UserId(model.created_by),
    )
    change.status = model.status
    change.impact_assessment = model.impact_assessment
    change.rollback_plan = model.rollback_plan
    change.implementation_schedule = model.implementation_schedule
    change.created_at = CreatedAt(model.created_at)
    change.updated_at = UpdatedAt(model.updated_at)
    change.implemented_at = model.implemented_at
    change.rolled_back_at = model.rolled_back_at
    change.approvals = json.loads(model.approvals) if model.approvals else []

    return change

  async def delete(self, change_id: str) -> None:
    stmt = select(ChangeRequestModel).where(ChangeRequestModel.id == change_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[ChangeRequest]:
    stmt = select(ChangeRequestModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    changes = []
    for model in models:
      change = ChangeRequest(
        change_id=model.id,
        title=Title(model.title),
        description=Description(model.description),
        change_type=model.change_type,
        risk_level=model.risk_level,
        created_by=UserId(model.created_by),
      )
      change.status = model.status
      change.impact_assessment = model.impact_assessment
      change.rollback_plan = model.rollback_plan
      change.implementation_schedule = model.implementation_schedule
      change.created_at = CreatedAt(model.created_at)
      change.updated_at = UpdatedAt(model.updated_at)
      change.implemented_at = model.implemented_at
      change.rolled_back_at = model.rolled_back_at
      change.approvals = json.loads(model.approvals) if model.approvals else []
      changes.append(change)

    return changes

  async def find_by_status(self, status: str) -> List[ChangeRequest]:
    stmt = select(ChangeRequestModel).where(ChangeRequestModel.status == status)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    changes = []
    for model in models:
      change = ChangeRequest(
        change_id=model.id,
        title=Title(model.title),
        description=Description(model.description),
        change_type=model.change_type,
        risk_level=model.risk_level,
        created_by=UserId(model.created_by),
      )
      change.status = model.status
      change.impact_assessment = model.impact_assessment
      change.rollback_plan = model.rollback_plan
      change.implementation_schedule = model.implementation_schedule
      change.created_at = CreatedAt(model.created_at)
      change.updated_at = UpdatedAt(model.updated_at)
      change.implemented_at = model.implemented_at
      change.rolled_back_at = model.rolled_back_at
      change.approvals = json.loads(model.approvals) if model.approvals else []
      changes.append(change)

    return changes

  async def find_by_risk_level(self, risk_level: str) -> List[ChangeRequest]:
    stmt = select(ChangeRequestModel).where(ChangeRequestModel.risk_level == risk_level)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    changes = []
    for model in models:
      change = ChangeRequest(
        change_id=model.id,
        title=Title(model.title),
        description=Description(model.description),
        change_type=model.change_type,
        risk_level=model.risk_level,
        created_by=UserId(model.created_by),
      )
      change.status = model.status
      change.impact_assessment = model.impact_assessment
      change.rollback_plan = model.rollback_plan
      change.implementation_schedule = model.implementation_schedule
      change.created_at = CreatedAt(model.created_at)
      change.updated_at = UpdatedAt(model.updated_at)
      change.implemented_at = model.implemented_at
      change.rolled_back_at = model.rolled_back_at
      change.approvals = json.loads(model.approvals) if model.approvals else []
      changes.append(change)

    return changes
