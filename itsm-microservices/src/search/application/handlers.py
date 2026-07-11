from uuid import uuid4
from ...shared.domain.domain_event import DomainEvent
from ..domain.search_index import SearchIndex
from ..infrastructure.repositories import SearchIndexRepository


class SearchIndexEventHandler:
  def __init__(self, repository: SearchIndexRepository):
    self.repository = repository

  async def handle_incident_created(self, event: DomainEvent) -> None:
    data = event.data
    index = SearchIndex(
      index_id=f"IDX-{uuid4().hex[:8].upper()}",
      entity_id=data.get("incident_id", ""),
      entity_type="INCIDENT",
      title=data.get("title", ""),
      description="Incident",
      content=f"Incident: {data.get('title', '')}",
      metadata={"priority": data.get("priority", "")},
    )
    await self.repository.save(index)

  async def handle_problem_identified(self, event: DomainEvent) -> None:
    data = event.data
    index = SearchIndex(
      index_id=f"IDX-{uuid4().hex[:8].upper()}",
      entity_id=data.get("problem_id", ""),
      entity_type="PROBLEM",
      title=data.get("title", ""),
      description="Problem",
      content=f"Problem: {data.get('title', '')}",
      metadata={},
    )
    await self.repository.save(index)

  async def handle_change_requested(self, event: DomainEvent) -> None:
    data = event.data
    index = SearchIndex(
      index_id=f"IDX-{uuid4().hex[:8].upper()}",
      entity_id=data.get("change_id", ""),
      entity_type="CHANGE",
      title=data.get("title", ""),
      description="Change Request",
      content=f"Change: {data.get('title', '')}",
      metadata={"change_type": data.get("change_type", "")},
    )
    await self.repository.save(index)

  async def handle_service_request_created(self, event: DomainEvent) -> None:
    data = event.data
    index = SearchIndex(
      index_id=f"IDX-{uuid4().hex[:8].upper()}",
      entity_id=data.get("request_id", ""),
      entity_type="REQUEST",
      title=data.get("title", ""),
      description="Service Request",
      content=f"Request: {data.get('title', '')}",
      metadata={"request_type": data.get("request_type", "")},
    )
    await self.repository.save(index)
