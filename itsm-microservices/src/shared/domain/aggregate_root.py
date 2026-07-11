from abc import ABC
from typing import List
from .domain_event import DomainEvent


class AggregateRoot(ABC):
  def __init__(self, aggregate_id: str):
    self.aggregate_id = aggregate_id
    self._events: List[DomainEvent] = []

  def add_event(self, event: DomainEvent) -> None:
    self._events.append(event)

  def get_events(self) -> List[DomainEvent]:
    return self._events.copy()

  def clear_events(self) -> None:
    self._events.clear()

  def has_events(self) -> bool:
    return len(self._events) > 0
