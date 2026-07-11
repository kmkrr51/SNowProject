from typing import Callable, List, Dict, Any
from ..domain.domain_event import DomainEvent


class EventBus:
  def __init__(self):
    self._handlers: Dict[str, List[Callable]] = {}

  def subscribe(self, event_type: str, handler: Callable) -> None:
    if event_type not in self._handlers:
      self._handlers[event_type] = []
    self._handlers[event_type].append(handler)

  async def publish(self, event: DomainEvent) -> None:
    event_type = event.__class__.__name__
    if event_type in self._handlers:
      for handler in self._handlers[event_type]:
        await handler(event)

  def get_handlers(self, event_type: str) -> List[Callable]:
    return self._handlers.get(event_type, [])


event_bus = EventBus()
