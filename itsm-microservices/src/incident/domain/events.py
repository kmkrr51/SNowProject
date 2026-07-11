from ...shared.domain.domain_event import DomainEvent


class IncidentCreated(DomainEvent):
  pass


class IncidentAssigned(DomainEvent):
  pass


class IncidentStatusChanged(DomainEvent):
  pass


class IncidentResolved(DomainEvent):
  pass


class IncidentClosed(DomainEvent):
  pass


class SLABreached(DomainEvent):
  pass


class SLAWarning(DomainEvent):
  pass
