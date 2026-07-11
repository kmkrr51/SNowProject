from uuid import uuid4
from ...shared.infrastructure import event_bus
from ...shared.domain.domain_event import DomainEvent
from ..domain.notification import Notification
from ..infrastructure.repositories import NotificationRepository


class NotificationEventHandler:
  def __init__(self, repository: NotificationRepository):
    self.repository = repository

  async def handle_incident_created(self, event: DomainEvent) -> None:
    data = event.data
    notification = Notification(
      notification_id=f"NOTIF-{uuid4().hex[:8].upper()}",
      recipient_id=data.get("created_by", ""),
      subject=f"Incident Created: {data.get('title', '')}",
      message=f"New incident {data.get('incident_id')} has been created",
      notification_type="INCIDENT_CREATED",
      related_entity_id=data.get("incident_id", ""),
      related_entity_type="INCIDENT",
    )
    await self.repository.save(notification)

  async def handle_incident_assigned(self, event: DomainEvent) -> None:
    data = event.data
    notification = Notification(
      notification_id=f"NOTIF-{uuid4().hex[:8].upper()}",
      recipient_id=data.get("assigned_to", ""),
      subject=f"Incident Assigned: {data.get('incident_id')}",
      message=f"Incident {data.get('incident_id')} has been assigned to you",
      notification_type="INCIDENT_ASSIGNED",
      related_entity_id=data.get("incident_id", ""),
      related_entity_type="INCIDENT",
    )
    await self.repository.save(notification)

  async def handle_change_approved(self, event: DomainEvent) -> None:
    data = event.data
    notification = Notification(
      notification_id=f"NOTIF-{uuid4().hex[:8].upper()}",
      recipient_id=data.get("approver_id", ""),
      subject=f"Change Approved: {data.get('change_id')}",
      message=f"Change {data.get('change_id')} has been approved",
      notification_type="CHANGE_APPROVED",
      related_entity_id=data.get("change_id", ""),
      related_entity_type="CHANGE",
    )
    await self.repository.save(notification)

  async def handle_service_request_fulfilled(self, event: DomainEvent) -> None:
    data = event.data
    notification = Notification(
      notification_id=f"NOTIF-{uuid4().hex[:8].upper()}",
      recipient_id=data.get("requester", ""),
      subject=f"Request Fulfilled: {data.get('request_id')}",
      message=f"Your service request {data.get('request_id')} has been fulfilled",
      notification_type="REQUEST_FULFILLED",
      related_entity_id=data.get("request_id", ""),
      related_entity_type="REQUEST",
    )
    await self.repository.save(notification)
