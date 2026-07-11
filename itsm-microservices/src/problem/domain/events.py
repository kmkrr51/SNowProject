from ...shared.domain.domain_event import DomainEvent


class ProblemIdentified(DomainEvent):
  pass


class RCAStarted(DomainEvent):
  pass


class RCACompleted(DomainEvent):
  pass


class KnownErrorCreated(DomainEvent):
  pass


class ProblemResolved(DomainEvent):
  pass
