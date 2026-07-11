from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...shared.domain import Repository, CreatedAt
from ..domain.notification import Notification
from .models import NotificationModel


class NotificationRepository(Repository[Notification]):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, notification: Notification) -> None:
    model = NotificationModel(
      id=notification.notification_id,
      recipient_id=notification.recipient_id,
      subject=notification.subject,
      message=notification.message,
      notification_type=notification.notification_type,
      related_entity_id=notification.related_entity_id,
      related_entity_type=notification.related_entity_type,
      status=notification.status,
      created_at=notification.created_at.value,
      read_at=notification.read_at,
    )
    self.session.add(model)
    await self.session.flush()

  async def get_by_id(self, notification_id: str) -> Optional[Notification]:
    stmt = select(NotificationModel).where(NotificationModel.id == notification_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()

    if not model:
      return None

    notification = Notification(
      notification_id=model.id,
      recipient_id=model.recipient_id,
      subject=model.subject,
      message=model.message,
      notification_type=model.notification_type,
      related_entity_id=model.related_entity_id,
      related_entity_type=model.related_entity_type,
    )
    notification.status = model.status
    notification.created_at = CreatedAt(model.created_at)
    notification.read_at = model.read_at

    return notification

  async def delete(self, notification_id: str) -> None:
    stmt = select(NotificationModel).where(NotificationModel.id == notification_id)
    result = await self.session.execute(stmt)
    model = result.scalar_one_or_none()
    if model:
      await self.session.delete(model)
      await self.session.flush()

  async def find_all(self) -> List[Notification]:
    stmt = select(NotificationModel)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    notifications = []
    for model in models:
      notification = Notification(
        notification_id=model.id,
        recipient_id=model.recipient_id,
        subject=model.subject,
        message=model.message,
        notification_type=model.notification_type,
        related_entity_id=model.related_entity_id,
        related_entity_type=model.related_entity_type,
      )
      notification.status = model.status
      notification.created_at = CreatedAt(model.created_at)
      notification.read_at = model.read_at
      notifications.append(notification)

    return notifications

  async def find_by_recipient(self, recipient_id: str) -> List[Notification]:
    stmt = select(NotificationModel).where(NotificationModel.recipient_id == recipient_id)
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    notifications = []
    for model in models:
      notification = Notification(
        notification_id=model.id,
        recipient_id=model.recipient_id,
        subject=model.subject,
        message=model.message,
        notification_type=model.notification_type,
        related_entity_id=model.related_entity_id,
        related_entity_type=model.related_entity_type,
      )
      notification.status = model.status
      notification.created_at = CreatedAt(model.created_at)
      notification.read_at = model.read_at
      notifications.append(notification)

    return notifications

  async def find_unread_by_recipient(self, recipient_id: str) -> List[Notification]:
    stmt = select(NotificationModel).where(
      (NotificationModel.recipient_id == recipient_id) & (NotificationModel.status == "UNREAD")
    )
    result = await self.session.execute(stmt)
    models = result.scalars().all()

    notifications = []
    for model in models:
      notification = Notification(
        notification_id=model.id,
        recipient_id=model.recipient_id,
        subject=model.subject,
        message=model.message,
        notification_type=model.notification_type,
        related_entity_id=model.related_entity_id,
        related_entity_type=model.related_entity_type,
      )
      notification.status = model.status
      notification.created_at = CreatedAt(model.created_at)
      notification.read_at = model.read_at
      notifications.append(notification)

    return notifications
