from ...shared.domain.domain_event import DomainEvent


class ServiceRequestCreated(DomainEvent):
  pass


class ServiceRequestAssigned(DomainEvent):
  pass


class ServiceRequestFulfilled(DomainEvent):
  pass


class ServiceRequestClosed(DomainEvent):
  pass
