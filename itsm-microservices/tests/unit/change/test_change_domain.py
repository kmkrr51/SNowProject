import pytest
from datetime import datetime, timedelta
from src.shared.domain import Title, Description, UserId
from src.change.domain.change_request import ChangeRequest


class TestChangeCreation:
  def test_create_change_successfully(self):
    change_id = "CHG-001"
    title = Title("Update database schema")
    description = Description("Add new columns to user table")
    change_type = "STANDARD"
    risk_level = "MEDIUM"
    created_by = UserId("user123")

    change = ChangeRequest(
      change_id=change_id,
      title=title,
      description=description,
      change_type=change_type,
      risk_level=risk_level,
      created_by=created_by,
    )

    assert change.change_id == change_id
    assert change.title == title
    assert change.description == description
    assert change.change_type == change_type
    assert change.risk_level == risk_level
    assert change.status == "DRAFT"
    assert change.has_events()

  def test_change_title_validation(self):
    with pytest.raises(ValueError):
      Title("")

    with pytest.raises(ValueError):
      Title("x" * 256)


class TestChangeApprovalWorkflow:
  def test_submit_change_for_approval(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.clear_events()
    change.submit_for_approval()

    assert change.status == "SUBMITTED"
    assert change.has_events()

  def test_cannot_submit_without_impact_assessment(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_rollback_plan("Revert schema changes")

    with pytest.raises(ValueError):
      change.submit_for_approval()

  def test_cannot_submit_without_rollback_plan(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")

    with pytest.raises(ValueError):
      change.submit_for_approval()

  def test_approve_change(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()
    change.clear_events()
    change.approve("approver123", "Looks good")

    assert change.is_approved()
    assert len(change.approvals) == 1
    assert change.approvals[0]["status"] == "APPROVED"
    assert change.has_events()

  def test_reject_change(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()
    change.clear_events()
    change.reject("approver123", "Need more testing")

    assert change.is_rejected()
    assert change.status == "REJECTED"
    assert change.has_events()

  def test_cannot_reject_without_reason(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()

    with pytest.raises(ValueError):
      change.reject("approver123", "")


class TestChangeImplementation:
  def test_implement_approved_change(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()
    change.approve("approver123")
    change.clear_events()
    change.implement()

    assert change.is_implemented()
    assert change.implemented_at is not None
    assert change.has_events()

  def test_cannot_implement_unapproved_change(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    with pytest.raises(ValueError):
      change.implement()


class TestChangeRollback:
  def test_rollback_implemented_change(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()
    change.approve("approver123")
    change.implement()
    change.clear_events()
    change.rollback()

    assert change.status == "ROLLED_BACK"
    assert change.rolled_back_at is not None
    assert change.has_events()

  def test_cannot_rollback_non_implemented_change(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    with pytest.raises(ValueError):
      change.rollback()


class TestChangeScheduling:
  def test_set_implementation_schedule(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    future_time = datetime.utcnow() + timedelta(days=1)
    change.set_implementation_schedule(future_time)

    assert change.implementation_schedule == future_time

  def test_cannot_schedule_in_past(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    past_time = datetime.utcnow() - timedelta(days=1)

    with pytest.raises(ValueError):
      change.set_implementation_schedule(past_time)


class TestChangeEvents:
  def test_change_requested_event(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    events = change.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ChangeRequested"

  def test_change_approval_requested_event(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.clear_events()
    change.submit_for_approval()

    events = change.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ChangeApprovalRequested"

  def test_change_approved_event(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()
    change.clear_events()
    change.approve("approver123")

    events = change.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ChangeApproved"

  def test_change_implemented_event(self):
    change = ChangeRequest(
      change_id="CHG-001",
      title=Title("Update database schema"),
      description=Description("Add new columns to user table"),
      change_type="STANDARD",
      risk_level="MEDIUM",
      created_by=UserId("user123"),
    )

    change.set_impact_assessment("Affects 5 services")
    change.set_rollback_plan("Revert schema changes")
    change.submit_for_approval()
    change.approve("approver123")
    change.clear_events()
    change.implement()

    events = change.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ChangeImplemented"
