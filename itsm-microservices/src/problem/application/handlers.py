from typing import Optional, List
from uuid import uuid4
from ...shared.domain import Title, Description, UserId
from ...shared.infrastructure import event_bus
from ..domain.problem import Problem
from ..domain.known_error import KnownError
from ..infrastructure.repositories import ProblemRepository, KnownErrorRepository
from .commands import (
  CreateProblemCommand,
  StartRCACommand,
  CompleteRCACommand,
  ResolveProblemCommand,
  AddRelatedIncidentCommand,
  AddImpactedServiceCommand,
  CreateKnownErrorCommand,
  DeactivateKnownErrorCommand,
)
from .queries import (
  GetProblemQuery,
  ListProblemsQuery,
  GetProblemsByStatusQuery,
  GetKnownErrorQuery,
  ListKnownErrorsQuery,
  GetKnownErrorsByProblemQuery,
)


class CreateProblemHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, command: CreateProblemCommand) -> str:
    problem_id = f"PROB-{uuid4().hex[:8].upper()}"

    problem = Problem(
      problem_id=problem_id,
      title=Title(command.title),
      description=Description(command.description),
      created_by=UserId(command.created_by),
    )

    await self.repository.save(problem)

    for event in problem.get_events():
      await event_bus.publish(event)

    problem.clear_events()

    return problem_id


class StartRCAHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, command: StartRCACommand) -> None:
    problem = await self.repository.get_by_id(command.problem_id)
    if not problem:
      raise ValueError(f"Problem {command.problem_id} not found")

    problem.start_rca()
    await self.repository.save(problem)

    for event in problem.get_events():
      await event_bus.publish(event)

    problem.clear_events()


class CompleteRCAHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, command: CompleteRCACommand) -> None:
    problem = await self.repository.get_by_id(command.problem_id)
    if not problem:
      raise ValueError(f"Problem {command.problem_id} not found")

    problem.complete_rca(command.root_cause)
    await self.repository.save(problem)

    for event in problem.get_events():
      await event_bus.publish(event)

    problem.clear_events()


class ResolveProblemHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, command: ResolveProblemCommand) -> None:
    problem = await self.repository.get_by_id(command.problem_id)
    if not problem:
      raise ValueError(f"Problem {command.problem_id} not found")

    problem.resolve()
    await self.repository.save(problem)

    for event in problem.get_events():
      await event_bus.publish(event)

    problem.clear_events()


class AddRelatedIncidentHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, command: AddRelatedIncidentCommand) -> None:
    problem = await self.repository.get_by_id(command.problem_id)
    if not problem:
      raise ValueError(f"Problem {command.problem_id} not found")

    problem.add_related_incident(command.incident_id)
    await self.repository.save(problem)


class AddImpactedServiceHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, command: AddImpactedServiceCommand) -> None:
    problem = await self.repository.get_by_id(command.problem_id)
    if not problem:
      raise ValueError(f"Problem {command.problem_id} not found")

    problem.add_impacted_service(command.service_name)
    await self.repository.save(problem)


class CreateKnownErrorHandler:
  def __init__(self, problem_repo: ProblemRepository, known_error_repo: KnownErrorRepository):
    self.problem_repo = problem_repo
    self.known_error_repo = known_error_repo

  async def handle(self, command: CreateKnownErrorCommand) -> str:
    problem = await self.problem_repo.get_by_id(command.problem_id)
    if not problem:
      raise ValueError(f"Problem {command.problem_id} not found")

    known_error_id = f"KE-{uuid4().hex[:8].upper()}"

    known_error = KnownError(
      known_error_id=known_error_id,
      problem_id=command.problem_id,
      workaround=command.workaround,
      temporary_fix=command.temporary_fix,
      permanent_fix=command.permanent_fix,
    )

    await self.known_error_repo.save(known_error)

    return known_error_id


class DeactivateKnownErrorHandler:
  def __init__(self, repository: KnownErrorRepository):
    self.repository = repository

  async def handle(self, command: DeactivateKnownErrorCommand) -> None:
    known_error = await self.repository.get_by_id(command.known_error_id)
    if not known_error:
      raise ValueError(f"Known error {command.known_error_id} not found")

    known_error.deactivate()
    await self.repository.save(known_error)


class GetProblemQueryHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, query: GetProblemQuery) -> Optional[Problem]:
    return await self.repository.get_by_id(query.problem_id)


class ListProblemsQueryHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, query: ListProblemsQuery) -> List[Problem]:
    problems = await self.repository.find_all()

    if query.status:
      problems = [p for p in problems if p.status.value == query.status]

    problems = problems[query.offset : query.offset + query.limit]

    return problems


class GetProblemsByStatusQueryHandler:
  def __init__(self, repository: ProblemRepository):
    self.repository = repository

  async def handle(self, query: GetProblemsByStatusQuery) -> List[Problem]:
    return await self.repository.find_by_status(query.status)


class GetKnownErrorQueryHandler:
  def __init__(self, repository: KnownErrorRepository):
    self.repository = repository

  async def handle(self, query: GetKnownErrorQuery) -> Optional[KnownError]:
    return await self.repository.get_by_id(query.known_error_id)


class ListKnownErrorsQueryHandler:
  def __init__(self, repository: KnownErrorRepository):
    self.repository = repository

  async def handle(self, query: ListKnownErrorsQuery) -> List[KnownError]:
    known_errors = await self.repository.find_all()

    if query.problem_id:
      known_errors = [ke for ke in known_errors if ke.problem_id == query.problem_id]

    known_errors = known_errors[query.offset : query.offset + query.limit]

    return known_errors


class GetKnownErrorsByProblemQueryHandler:
  def __init__(self, repository: KnownErrorRepository):
    self.repository = repository

  async def handle(self, query: GetKnownErrorsByProblemQuery) -> List[KnownError]:
    return await self.repository.find_by_problem_id(query.problem_id)
