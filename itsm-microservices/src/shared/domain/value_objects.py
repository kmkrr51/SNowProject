from dataclasses import dataclass
from typing import Any
from enum import Enum
from datetime import datetime, timedelta


class Priority(str, Enum):
  CRITICAL = "CRITICAL"
  HIGH = "HIGH"
  MEDIUM = "MEDIUM"
  LOW = "LOW"


class Status(str, Enum):
  NEW = "NEW"
  ASSIGNED = "ASSIGNED"
  IN_PROGRESS = "IN_PROGRESS"
  RESOLVED = "RESOLVED"
  CLOSED = "CLOSED"


class ImpactLevel(str, Enum):
  HIGH = "HIGH"
  MEDIUM = "MEDIUM"
  LOW = "LOW"


class UrgencyLevel(str, Enum):
  HIGH = "HIGH"
  MEDIUM = "MEDIUM"
  LOW = "LOW"


class Availability(str, Enum):
  AVAILABLE = "AVAILABLE"
  BUSY = "BUSY"
  ON_LEAVE = "ON_LEAVE"


@dataclass(frozen=True)
class IncidentId:
  value: str

  def __str__(self) -> str:
    return self.value


@dataclass(frozen=True)
class TechnicianId:
  value: str

  def __str__(self) -> str:
    return self.value


@dataclass(frozen=True)
class SLAId:
  value: str

  def __str__(self) -> str:
    return self.value


@dataclass(frozen=True)
class WorkNoteId:
  value: str

  def __str__(self) -> str:
    return self.value


@dataclass(frozen=True)
class Title:
  value: str

  def __post_init__(self):
    if not self.value or len(self.value.strip()) == 0:
      raise ValueError("Title cannot be empty")
    if len(self.value) > 255:
      raise ValueError("Title cannot exceed 255 characters")


@dataclass(frozen=True)
class Description:
  value: str

  def __post_init__(self):
    if not self.value or len(self.value.strip()) == 0:
      raise ValueError("Description cannot be empty")


@dataclass(frozen=True)
class Duration:
  hours: int
  minutes: int = 0

  def __post_init__(self):
    if self.hours < 0 or self.minutes < 0:
      raise ValueError("Duration cannot be negative")
    if self.minutes >= 60:
      raise ValueError("Minutes must be less than 60")

  def to_timedelta(self) -> timedelta:
    return timedelta(hours=self.hours, minutes=self.minutes)

  def __str__(self) -> str:
    return f"{self.hours:02d}:{self.minutes:02d}"


@dataclass(frozen=True)
class SLAInfo:
  response_time: Duration
  resolution_time: Duration

  def __post_init__(self):
    if self.response_time.to_timedelta() >= self.resolution_time.to_timedelta():
      raise ValueError("Response time must be less than resolution time")


@dataclass(frozen=True)
class CreatedAt:
  value: datetime

  def __post_init__(self):
    if self.value > datetime.utcnow():
      raise ValueError("Created time cannot be in the future")


@dataclass(frozen=True)
class UpdatedAt:
  value: datetime

  def __post_init__(self):
    if self.value > datetime.utcnow():
      raise ValueError("Updated time cannot be in the future")


@dataclass(frozen=True)
class UserId:
  value: str

  def __str__(self) -> str:
    return self.value
