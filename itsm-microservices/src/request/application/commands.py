from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateServiceRequestCommand:
  request_type: str
  title: str
  description: str
  requester: str
  requested_service: str
  priority: str


@dataclass
class AssignServiceRequestCommand:
  request_id: str
  technician_id: str


@dataclass
class AddTaskCommand:
  request_id: str
  task_name: str
  description: str


@dataclass
class CompleteTaskCommand:
  request_id: str
  task_index: int


@dataclass
class FulfillServiceRequestCommand:
  request_id: str
  fulfillment_details: str


@dataclass
class CloseServiceRequestCommand:
  request_id: str
