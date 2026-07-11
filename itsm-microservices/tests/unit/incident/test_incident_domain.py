import pytest
from datetime import datetime
from src.shared.domain import (
  IncidentId,
  Title,
  Description,
  Priority,
  ImpactLevel,
  UrgencyLevel,
  TechnicianId,
  UserId,
  Status,
)
from src.incident.domain.incident import Incident


class TestIncidentCreation:
  def test_create_incident_successfully(self):
    incident_id = IncidentId("INC-001")
    title = Title("Email not working")
    description = Description("User cannot access email")
    priority = Priority.HIGH
    impact_level = ImpactLevel.HIGH
    urgency_level = UrgencyLevel.HIGH
    created_by = UserId("user123")

    incident = Incident(
      incident_id=incident_id,
      title=title,
      description=description,
      priority=priority,
      impact_level=impact_level,
      urgency_level=urgency_level,
      created_by=created_by,
    )

    assert incident.incident_id == incident_id
    assert incident.title == title
    assert incident.description == description
    assert incident.priority == priority
    assert incident.status == Status.NEW
    assert incident.impact_level == impact_level
    assert incident.urgency_level == urgency_level
    assert incident.created_by == created_by
    assert incident.has_events()

  def test_incident_title_validation(self):
    with pytest.raises(ValueError):
      Title("")

    with pytest.raises(ValueError):
      Title("x" * 256)

  def test_incident_description_validation(self):
    with pytest.raises(ValueError):
      Description("")


class TestIncidentAssignment:
  def test_assign_incident_successfully(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    technician_id = TechnicianId("TECH-001")
    incident.assign_to(technician_id)

    assert incident.assigned_to == technician_id
    assert incident.status == Status.ASSIGNED
    assert incident.is_assigned()

  def test_cannot_assign_already_assigned_incident(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    incident.assign_to(TechnicianId("TECH-001"))

    with pytest.raises(ValueError):
      incident.assign_to(TechnicianId("TECH-002"))


class TestIncidentStatusChange:
  def test_change_status_successfully(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    incident.change_status(Status.IN_PROGRESS)
    assert incident.status == Status.IN_PROGRESS

    incident.change_status(Status.RESOLVED)
    assert incident.status == Status.RESOLVED
    assert incident.is_resolved()
    assert incident.resolved_at is not None

  def test_cannot_change_to_same_status(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    with pytest.raises(ValueError):
      incident.change_status(Status.NEW)

  def test_close_incident(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    incident.change_status(Status.CLOSED)
    assert incident.status == Status.CLOSED
    assert incident.is_closed()
    assert incident.closed_at is not None


class TestIncidentEvents:
  def test_incident_created_event(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    events = incident.get_events()
    assert len(events) == 1
    assert events[0].event_type == "IncidentCreated"

  def test_incident_assigned_event(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    incident.clear_events()
    incident.assign_to(TechnicianId("TECH-001"))

    events = incident.get_events()
    assert len(events) == 1
    assert events[0].event_type == "IncidentAssigned"

  def test_incident_status_changed_event(self):
    incident = Incident(
      incident_id=IncidentId("INC-001"),
      title=Title("Email not working"),
      description=Description("User cannot access email"),
      priority=Priority.HIGH,
      impact_level=ImpactLevel.HIGH,
      urgency_level=UrgencyLevel.HIGH,
      created_by=UserId("user123"),
    )

    incident.clear_events()
    incident.change_status(Status.IN_PROGRESS)

    events = incident.get_events()
    assert len(events) == 1
    assert events[0].event_type == "IncidentStatusChanged"
