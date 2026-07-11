from typing import Optional, List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from ...shared.domain import Repository, CreatedAt
from ..domain.search_index import SearchIndex
from .models import SearchIndexModel


class SearchIndexRepository(Repository[SearchIndex]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, index: SearchIndex) -> None:
    model = SearchIndexModel(
      id=index.index_id,
      entity_id=index.entity_id,
      entity_type=index.entity_type,
      title=index.title,
      description=index.description,
      content=index.content,
      metadata=json.dumps(index.metadata) if index.metadata else None,
      created_at=index.created_at.value,
      updated_at=index.updated_at,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, index_id: str) -> Optional[SearchIndex]:
    stmt = select(SearchIndexModel).where(SearchIndexModel.id == index_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    return self._model_to_domain(model)

  async def delete(self, index_id: str) -> None:
    stmt = select(SearchIndexModel).where(SearchIndexModel.id == index_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[SearchIndex]:
    stmt = select(SearchIndexModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()
    return [self._model_to_domain(m) for m in models]

  async def search(self, query: str, entity_type: Optional[str] = None) -> List[SearchIndex]:
    search_term = f"%{query}%"
    stmt = select(SearchIndexModel).where(
      or_(
        SearchIndexModel.title.ilike(search_term),
        SearchIndexModel.description.ilike(search_term),
        SearchIndexModel.content.ilike(search_term),
      )
    )

    if entity_type:
      stmt = stmt.where(SearchIndexModel.entity_type == entity_type)

    result = await self.session.execute(stmt)
    models = result.scalars().all()
    return [self._model_to_domain(m) for m in models]

  def _model_to_domain(self, model: SearchIndexModel) -> SearchIndex:
    index = SearchIndex(
      index_id=model.id,
      entity_id=model.entity_id,
      entity_type=model.entity_type,
      title=model.title,
      description=model.description,
      content=model.content,
      metadata=json.loads(model.metadata) if model.metadata else {},
    )
    index.created_at = CreatedAt(model.created_at)
    index.updated_at = model.updated_at
    return index
