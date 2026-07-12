from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
  CreateProblemRequest,
  StartRCARequest,
  CompleteRCARequest,
  AddRelatedIncidentRequest,
  AddImpactedServiceRequest,
  CreateKnownErrorRequest,
  ProblemResponse,
  KnownErrorResponse,
  ProblemListResponse,
  KnownErrorListResponse,
  ErrorResponse,
)
from ..application.commands import (
  CreateProblemCommand,
  StartRCACommand,
  CompleteRCACommand,
  ResolveProblemCommand,
  AddRelatedIncidentCommand,
  AddImpactedServiceCommand,
  CreateKnownErrorCommand,
  DeactivateKnownErrorCommand,
)
from ..application.queries import (
  GetProblemQuery,
  ListProblemsQuery,
  GetKnownErrorQuery,
  GetKnownErrorsByProblemQuery,
)
from ..infrastructure.repositories import ProblemRepository, KnownErrorRepository
from ..application.handlers import (
  CreateProblemHandler,
  StartRCAHandler,
  CompleteRCAHandler,
  ResolveProblemHandler,
  AddRelatedIncidentHandler,
  AddImpactedServiceHandler,
  CreateKnownErrorHandler,
  DeactivateKnownErrorHandler,
  GetProblemQueryHandler,
  ListProblemsQueryHandler,
  GetKnownErrorQueryHandler,
  GetKnownErrorsByProblemQueryHandler,
)

router = APIRouter(prefix="/api/v1/problems", tags=["problems"])


async def get_session():
  from ...shared.infrastructure import get_database_engine, get_session_factory
  engine = await get_database_engine()
  factory = await get_session_factory(engine)
  async with factory() as session:
    yield session


@router.post("", response_model=dict, status_code=201)
async def create_problem(
  request: CreateProblemRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = CreateProblemHandler(repository)

    command = CreateProblemCommand(
      title=request.title,
      description=request.description,
      created_by=request.created_by,
    )

    problem_id = await handler.handle(command)
    await session.commit()

    return {"id": problem_id, "message": "Problem created successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
  problem_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = GetProblemQueryHandler(repository)

    query = GetProblemQuery(problem_id=problem_id)
    problem = await handler.handle(query)

    if not problem:
      raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found")

    return ProblemResponse(
      id=problem.problem_id,
      title=problem.title.value,
      description=problem.description.value,
      status=problem.status.value,
      root_cause=problem.root_cause,
      created_by=str(problem.created_by),
      created_at=problem.created_at.value,
      updated_at=problem.updated_at.value,
      resolved_at=problem.resolved_at,
      related_incidents=problem.related_incidents,
      impacted_services=problem.impacted_services,
    )
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ProblemListResponse)
async def list_problems(
  status: Optional[str] = Query(None),
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = ListProblemsQueryHandler(repository)

    query = ListProblemsQuery(
      status=status,
      limit=limit,
      offset=offset,
    )
    result = await handler.handle(query)

    problems = [
      ProblemResponse(
        id=problem.problem_id,
        title=problem.title.value,
        description=problem.description.value,
        status=problem.status.value,
        root_cause=problem.root_cause,
        created_by=str(problem.created_by),
        created_at=problem.created_at.value,
        updated_at=problem.updated_at.value,
        resolved_at=problem.resolved_at,
        related_incidents=problem.related_incidents,
        impacted_services=problem.impacted_services,
      )
      for problem in result.get("problems", [])
    ]

    return ProblemListResponse(
      problems=problems,
      total=result.get("total", 0),
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{problem_id}/rca/start", status_code=200)
async def start_rca(
  problem_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = StartRCAHandler(repository)

    command = StartRCACommand(problem_id=problem_id)
    await handler.handle(command)
    await session.commit()

    return {"message": "RCA started successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{problem_id}/rca/complete", status_code=200)
async def complete_rca(
  problem_id: str,
  request: CompleteRCARequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = CompleteRCAHandler(repository)

    command = CompleteRCACommand(
      problem_id=problem_id,
      root_cause=request.root_cause,
    )
    await handler.handle(command)
    await session.commit()

    return {"message": "RCA completed successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{problem_id}/resolve", status_code=200)
async def resolve_problem(
  problem_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = ResolveProblemHandler(repository)

    command = ResolveProblemCommand(problem_id=problem_id)
    await handler.handle(command)
    await session.commit()

    return {"message": "Problem resolved successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{problem_id}/related-incidents", status_code=200)
async def add_related_incident(
  problem_id: str,
  request: AddRelatedIncidentRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = AddRelatedIncidentHandler(repository)

    command = AddRelatedIncidentCommand(
      problem_id=problem_id,
      incident_id=request.incident_id,
    )
    await handler.handle(command)
    await session.commit()

    return {"message": "Related incident added successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{problem_id}/impacted-services", status_code=200)
async def add_impacted_service(
  problem_id: str,
  request: AddImpactedServiceRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = ProblemRepository(session)
    handler = AddImpactedServiceHandler(repository)

    command = AddImpactedServiceCommand(
      problem_id=problem_id,
      service_name=request.service_name,
    )
    await handler.handle(command)
    await session.commit()

    return {"message": "Impacted service added successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{problem_id}/known-errors", response_model=dict, status_code=201)
async def create_known_error(
  problem_id: str,
  request: CreateKnownErrorRequest,
  session: AsyncSession = Depends(get_session),
):
  try:
    problem_repo = ProblemRepository(session)
    known_error_repo = KnownErrorRepository(session)
    handler = CreateKnownErrorHandler(problem_repo, known_error_repo)

    command = CreateKnownErrorCommand(
      problem_id=problem_id,
      workaround=request.workaround,
      temporary_fix=request.temporary_fix,
      permanent_fix=request.permanent_fix,
    )

    known_error_id = await handler.handle(command)
    await session.commit()

    return {"id": known_error_id, "message": "Known error created successfully"}
  except ValueError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/{problem_id}/known-errors", response_model=KnownErrorListResponse)
async def get_known_errors_by_problem(
  problem_id: str,
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = KnownErrorRepository(session)
    handler = GetKnownErrorsByProblemQueryHandler(repository)

    query = GetKnownErrorsByProblemQuery(problem_id=problem_id)
    known_errors = await handler.handle(query)
    all_known_errors = await repository.find_all()

    return KnownErrorListResponse(
      known_errors=[
        KnownErrorResponse(
          id=ke.known_error_id,
          problem_id=ke.problem_id,
          workaround=ke.workaround,
          temporary_fix=ke.temporary_fix,
          permanent_fix=ke.permanent_fix,
          status=ke.status,
          created_at=ke.created_at.value,
          updated_at=ke.updated_at.value,
        )
        for ke in known_errors
      ],
      total=len(all_known_errors),
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
