import pytest
from src.shared.domain import Title, Description, UserId
from src.request.domain.service_request import ServiceRequest


class TestServiceRequestCreation:
  def test_create_service_request_successfully(self):
    request_id = "REQ-001"
    request_type = "STANDARD"
    title = Title("Request for new laptop")
    description = Description("Need a new laptop for development")
    requester = UserId("user123")
    requested_service = "IT Hardware"
    priority = "HIGH"

    req = ServiceRequest(
      request_id=request_id,
      request_type=request_type,
      title=title,
      description=description,
      requester=requester,
      requested_service=requested_service,
      priority=priority,
    )

    assert req.request_id == request_id
    assert req.request_type == request_type
    assert req.title == title
    assert req.description == description
    assert req.requester == requester
    assert req.requested_service == requested_service
    assert req.priority == priority
    assert req.status == "NEW"
    assert req.has_events()

  def test_service_request_title_validation(self):
    with pytest.raises(ValueError):
      Title("")

    with pytest.raises(ValueError):
      Title("x" * 256)


class TestServiceRequestAssignment:
  def test_assign_service_request(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.assign_to("tech123")

    assert req.is_assigned()
    assert req.assigned_to == "tech123"
    assert req.status == "ASSIGNED"

  def test_cannot_assign_already_assigned_request(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.assign_to("tech123")

    with pytest.raises(ValueError):
      req.assign_to("tech456")


class TestServiceRequestTasks:
  def test_add_task(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.add_task("Verify specifications", "Check laptop specs with user")
    req.add_task("Order laptop", "Place order with vendor")

    assert len(req.tasks) == 2
    assert req.tasks[0]["name"] == "Verify specifications"
    assert req.tasks[0]["status"] == "PENDING"

  def test_cannot_add_empty_task(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    with pytest.raises(ValueError):
      req.add_task("", "Description")

  def test_complete_task(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.add_task("Verify specifications", "Check laptop specs with user")
    req.add_task("Order laptop", "Place order with vendor")
    req.complete_task(0)

    assert req.tasks[0]["status"] == "COMPLETED"
    assert "completed_at" in req.tasks[0]

  def test_cannot_complete_invalid_task(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    with pytest.raises(ValueError):
      req.complete_task(0)

  def test_get_progress(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    assert req.get_progress() == 0.0

    req.add_task("Task 1", "Description 1")
    req.add_task("Task 2", "Description 2")

    assert req.get_progress() == 0.0

    req.complete_task(0)
    assert req.get_progress() == 50.0

    req.complete_task(1)
    assert req.get_progress() == 100.0


class TestServiceRequestFulfillment:
  def test_fulfill_service_request(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.fulfill("Laptop delivered and configured")

    assert req.is_fulfilled()
    assert req.fulfillment_details == "Laptop delivered and configured"
    assert req.fulfilled_at is not None

  def test_cannot_fulfill_already_fulfilled_request(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.fulfill("Laptop delivered and configured")

    with pytest.raises(ValueError):
      req.fulfill("Another fulfillment")

  def test_cannot_fulfill_with_empty_details(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    with pytest.raises(ValueError):
      req.fulfill("")


class TestServiceRequestClosure:
  def test_close_service_request(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.close()

    assert req.is_closed()
    assert req.closed_at is not None

  def test_cannot_close_already_closed_request(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.close()

    with pytest.raises(ValueError):
      req.close()


class TestServiceRequestEvents:
  def test_service_request_created_event(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    events = req.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ServiceRequestCreated"

  def test_service_request_assigned_event(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.clear_events()
    req.assign_to("tech123")

    events = req.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ServiceRequestAssigned"

  def test_service_request_fulfilled_event(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.clear_events()
    req.fulfill("Laptop delivered")

    events = req.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ServiceRequestFulfilled"

  def test_service_request_closed_event(self):
    req = ServiceRequest(
      request_id="REQ-001",
      request_type="STANDARD",
      title=Title("Request for new laptop"),
      description=Description("Need a new laptop for development"),
      requester=UserId("user123"),
      requested_service="IT Hardware",
      priority="HIGH",
    )

    req.clear_events()
    req.close()

    events = req.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ServiceRequestClosed"
