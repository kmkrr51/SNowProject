from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import SearchResponse, SearchResultResponse
from ..infrastructure.repositories import SearchIndexRepository

router = APIRouter(prefix="/api/v1/search", tags=["search"])


async def get_session():
  from ...shared.infrastructure import get_database_engine, get_session_factory
  engine = await get_database_engine()
  factory = await get_session_factory(engine)
  async with factory() as session:
    yield session


@router.get("", response_model=SearchResponse)
async def search(
  q: str = Query(..., min_length=1),
  entity_type: Optional[str] = Query(None),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = SearchIndexRepository(session)
    results = await repository.search(q, entity_type)

    return SearchResponse(
      results=[
        SearchResultResponse(
          id=r.index_id,
          entity_id=r.entity_id,
          entity_type=r.entity_type,
          title=r.title,
          description=r.description,
          metadata=r.metadata,
          created_at=r.created_at.value,
          updated_at=r.updated_at,
        )
        for r in results
      ],
      total=len(results),
      query=q,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
