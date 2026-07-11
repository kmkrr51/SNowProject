from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import NotificationResponse, NotificationListResponse
from ..infrastructure.repositories import NotificationRepository

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


async def get_session():
  from ...shared.infrastructure import get_database_engine, get_session_factory
  engine = await get_database_engine()
  factory = await get_session_factory(engine)
  async with factory() as session:
    yield session


@router.get("/recipient/{recipient_id}", response_model=NotificationListResponse)
async def get_notifications_for_recipient(
  recipient_id: str,
  limit: int = Query(100, ge=1, le=1000),
  offset: int = Query(0, ge=0),
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = NotificationRepository(session)
    notifications = await repository.find_by_recipient(recipient_id)
    unread = await repository.find_unread_by_recipient(recipient_id)

    paginated = notifications[offset : offset + limit]

    return NotificationListResponse(
      notifications=[
        NotificationResponse(
          id=n.notification_id,
          recipient_id=n.recipient_id,
          subject=n.subject,
          message=n.message,
          notification_type=n.notification_type,
          related_entity_id=n.related_entity_id,
          related_entity_type=n.related_entity_type,
          status=n.status,
          created_at=n.created_at.value,
          read_at=n.read_at,
        )
        for n in paginated
      ],
      total=len(notifications),
      unread_count=len(unread),
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/{notification_id}/mark-as-read", status_code=200)
async def mark_notification_as_read(
  notification_id: str,
  session: AsyncSession = Depends(get_session),
):
  try:
    repository = NotificationRepository(session)
    notification = await repository.get_by_id(notification_id)

    if not notification:
      raise HTTPException(status_code=404, detail=f"Notification {notification_id} not found")

    notification.mark_as_read()
    await repository.save(notification)
    await session.commit()

    return {"message": "Notification marked as read"}
  except HTTPException:
    raise
  except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
