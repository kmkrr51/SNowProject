from ...shared.domain.domain_event import DomainEvent


class ChangeRequested(DomainEvent):
  pass


class ChangeApprovalRequested(DomainEvent):
  pass


class ChangeApproved(DomainEvent):
  pass


class ChangeRejected(DomainEvent):
  pass


class ChangeImplemented(DomainEvent):
  pass


class ChangeRolledBack(DomainEvent):
  pass
