from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ...shared.infrastructure import get_database_engine, get_session_factory
from ..infrastructure.repositories import IncidentRepository
from ..application.handlers import (
  CreateIncidentHandler,
  AssignIncidentHandler,
  ChangeIncidentStatusHandler,
  ResolveIncidentHandler,
  CloseIncidentHandler,
  GetIncidentQueryHandler,
  ListIncidentsQueryHandler,
  GetIncidentsByStatusQueryHandler,
  GetIncidentsByTechnicianQueryHandler,
)

_session_factory = None


async def init_session_factory():
  global _session_factory
  engine = await get_database_engine()
  _session_factory = await get_session_factory(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
  if _session_factory is None:
    await init_session_factory()

  async with _session_factory() as session:
    yield session


async def get_incident_repository(session: AsyncSession = None) -> IncidentRepository:
  if session is None:
    async for session in get_session():
      return IncidentRepository(session)
  return IncidentRepository(session)


async def get_create_incident_handler(
  repository: IncidentRepository = None,
) -> CreateIncidentHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return CreateIncidentHandler(repo)
  return CreateIncidentHandler(repository)


async def get_assign_incident_handler(
  repository: IncidentRepository = None,
) -> AssignIncidentHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return AssignIncidentHandler(repo)
  return AssignIncidentHandler(repository)


async def get_change_status_handler(
  repository: IncidentRepository = None,
) -> ChangeIncidentStatusHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return ChangeIncidentStatusHandler(repo)
  return ChangeIncidentStatusHandler(repository)


async def get_resolve_handler(
  repository: IncidentRepository = None,
) -> ResolveIncidentHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return ResolveIncidentHandler(repo)
  return ResolveIncidentHandler(repository)


async def get_close_handler(
  repository: IncidentRepository = None,
) -> CloseIncidentHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return CloseIncidentHandler(repo)
  return CloseIncidentHandler(repository)


async def get_get_incident_handler(
  repository: IncidentRepository = None,
) -> GetIncidentQueryHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return GetIncidentQueryHandler(repo)
  return GetIncidentQueryHandler(repository)


async def get_list_incidents_handler(
  repository: IncidentRepository = None,
) -> ListIncidentsQueryHandler:
  if repository is None:
    async for repo in get_incident_repository():
      return ListIncidentsQueryHandler(repo)
  return ListIncidentsQueryHandler(repository)
