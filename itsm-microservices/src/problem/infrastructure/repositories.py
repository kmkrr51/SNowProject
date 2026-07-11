from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...shared.domain import Repository, Title, Description, UserId, CreatedAt, UpdatedAt
from ..domain.problem import Problem
from ..domain.known_error import KnownError
from .models import ProblemModel, KnownErrorModel


class ProblemRepository(Repository[Problem]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, problem: Problem) -> None:
    model = ProblemModel(
      id=problem.problem_id,
      title=problem.title.value,
      description=problem.description.value,
      status=problem.status.value,
      root_cause=problem.root_cause,
      created_by=str(problem.created_by),
      created_at=problem.created_at.value,
      updated_at=problem.updated_at.value,
      resolved_at=problem.resolved_at,
      related_incidents=",".join(problem.related_incidents) if problem.related_incidents else None,
      impacted_services=",".join(problem.impacted_services) if problem.impacted_services else None,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, problem_id: str) -> Optional[Problem]:
    stmt = select(ProblemModel).where(ProblemModel.id == problem_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    problem = Problem(
      problem_id=model.id,
      title=Title(model.title),
      description=Description(model.description),
      created_by=UserId(model.created_by),
    )
    problem.status = model.status
    problem.root_cause = model.root_cause
    problem.created_at = CreatedAt(model.created_at)
    problem.updated_at = UpdatedAt(model.updated_at)
    problem.resolved_at = model.resolved_at
    problem.related_incidents = model.related_incidents.split(",") if model.related_incidents else []
    problem.impacted_services = model.impacted_services.split(",") if model.impacted_services else []

    return problem

  async def delete(self, problem_id: str) -> None:
    stmt = select(ProblemModel).where(ProblemModel.id == problem_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[Problem]:
    stmt = select(ProblemModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    problems = []
    for model in models:
      problem = Problem(
        problem_id=model.id,
        title=Title(model.title),
        description=Description(model.description),
        created_by=UserId(model.created_by),
      )
      problem.status = model.status
      problem.root_cause = model.root_cause
      problem.created_at = CreatedAt(model.created_at)
      problem.updated_at = UpdatedAt(model.updated_at)
      problem.resolved_at = model.resolved_at
      problem.related_incidents = model.related_incidents.split(",") if model.related_incidents else []
      problem.impacted_services = model.impacted_services.split(",") if model.impacted_services else []
      problems.append(problem)

    return problems

  async def find_by_status(self, status: str) -> List[Problem]:
    stmt = select(ProblemModel).where(ProblemModel.status == status)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    problems = []
    for model in models:
      problem = Problem(
        problem_id=model.id,
        title=Title(model.title),
        description=Description(model.description),
        created_by=UserId(model.created_by),
      )
      problem.status = model.status
      problem.root_cause = model.root_cause
      problem.created_at = CreatedAt(model.created_at)
      problem.updated_at = UpdatedAt(model.updated_at)
      problem.resolved_at = model.resolved_at
      problem.related_incidents = model.related_incidents.split(",") if model.related_incidents else []
      problem.impacted_services = model.impacted_services.split(",") if model.impacted_services else []
      problems.append(problem)

    return problems


class KnownErrorRepository(Repository[KnownError]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, known_error: KnownError) -> None:
    model = KnownErrorModel(
      id=known_error.known_error_id,
      problem_id=known_error.problem_id,
      workaround=known_error.workaround,
      temporary_fix=known_error.temporary_fix,
      permanent_fix=known_error.permanent_fix,
      status=known_error.status,
      created_at=known_error.created_at.value,
      updated_at=known_error.updated_at.value,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, known_error_id: str) -> Optional[KnownError]:
    stmt = select(KnownErrorModel).where(KnownErrorModel.id == known_error_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    return KnownError(
      known_error_id=model.id,
      problem_id=model.problem_id,
      workaround=model.workaround,
      temporary_fix=model.temporary_fix,
      permanent_fix=model.permanent_fix,
    )

  async def delete(self, known_error_id: str) -> None:
    stmt = select(KnownErrorModel).where(KnownErrorModel.id == known_error_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[KnownError]:
    stmt = select(KnownErrorModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    return [
      KnownError(
        known_error_id=model.id,
        problem_id=model.problem_id,
        workaround=model.workaround,
        temporary_fix=model.temporary_fix,
        permanent_fix=model.permanent_fix,
      )
      for model in models
    ]

  async def find_by_problem_id(self, problem_id: str) -> List[KnownError]:
    stmt = select(KnownErrorModel).where(KnownErrorModel.problem_id == problem_id)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    return [
      KnownError(
        known_error_id=model.id,
        problem_id=model.problem_id,
        workaround=model.workaround,
        temporary_fix=model.temporary_fix,
        permanent_fix=model.permanent_fix,
      )
      for model in models
    ]
