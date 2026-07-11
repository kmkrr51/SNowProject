from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from .aggregate_root import AggregateRoot


T = TypeVar("T", bound=AggregateRoot)


class Repository(ABC, Generic[T]):
  @abstractmethod
  async def save(self, aggregate: T) -> None:
    pass

  @abstractmethod
  async def get_by_id(self, aggregate_id: str) -> Optional[T]:
    pass

  @abstractmethod
  async def delete(self, aggregate_id: str) -> None:
    pass

  @abstractmethod
  async def find_all(self) -> List[T]:
    pass
