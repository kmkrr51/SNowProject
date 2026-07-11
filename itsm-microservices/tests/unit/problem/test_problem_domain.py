import pytest
from src.shared.domain import Title, Description, UserId
from src.problem.domain.problem import Problem
from src.problem.domain.known_error import KnownError


class TestProblemCreation:
  def test_create_problem_successfully(self):
    problem_id = "PROB-001"
    title = Title("Database connection timeout")
    description = Description("Database connections timing out intermittently")
    created_by = UserId("user123")

    problem = Problem(
      problem_id=problem_id,
      title=title,
      description=description,
      created_by=created_by,
    )

    assert problem.problem_id == problem_id
    assert problem.title == title
    assert problem.description == description
    assert problem.created_by == created_by
    assert problem.has_events()
    assert not problem.is_resolved()

  def test_problem_title_validation(self):
    with pytest.raises(ValueError):
      Title("")

    with pytest.raises(ValueError):
      Title("x" * 256)


class TestRCAWorkflow:
  def test_start_rca_successfully(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.clear_events()
    problem.start_rca()

    assert problem.status.value == "IN_PROGRESS"
    assert problem.has_events()

  def test_complete_rca_successfully(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.start_rca()
    problem.clear_events()
    problem.complete_rca("Connection pool exhaustion due to memory leak")

    assert problem.has_root_cause()
    assert problem.root_cause == "Connection pool exhaustion due to memory leak"
    assert problem.has_events()

  def test_cannot_complete_rca_without_starting(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    with pytest.raises(ValueError):
      problem.complete_rca("Some root cause")

  def test_cannot_complete_rca_with_empty_root_cause(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.start_rca()

    with pytest.raises(ValueError):
      problem.complete_rca("")


class TestProblemResolution:
  def test_resolve_problem_successfully(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.resolve()

    assert problem.is_resolved()
    assert problem.resolved_at is not None
    assert problem.has_events()

  def test_cannot_resolve_already_resolved_problem(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.resolve()

    with pytest.raises(ValueError):
      problem.resolve()


class TestRelatedIncidents:
  def test_add_related_incident(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.add_related_incident("INC-001")
    problem.add_related_incident("INC-002")

    assert len(problem.related_incidents) == 2
    assert "INC-001" in problem.related_incidents
    assert "INC-002" in problem.related_incidents

  def test_cannot_add_duplicate_incident(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.add_related_incident("INC-001")
    problem.add_related_incident("INC-001")

    assert len(problem.related_incidents) == 1


class TestImpactedServices:
  def test_add_impacted_service(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.add_impacted_service("Email Service")
    problem.add_impacted_service("Calendar Service")

    assert len(problem.impacted_services) == 2
    assert "Email Service" in problem.impacted_services
    assert "Calendar Service" in problem.impacted_services


class TestKnownError:
  def test_create_known_error(self):
    known_error = KnownError(
      known_error_id="KE-001",
      problem_id="PROB-001",
      workaround="Restart the database connection pool",
      temporary_fix="Increase connection pool size",
      permanent_fix="Fix memory leak in connection pooling code",
    )

    assert known_error.known_error_id == "KE-001"
    assert known_error.problem_id == "PROB-001"
    assert known_error.is_active()

  def test_deactivate_known_error(self):
    known_error = KnownError(
      known_error_id="KE-001",
      problem_id="PROB-001",
      workaround="Restart the database connection pool",
      temporary_fix="Increase connection pool size",
      permanent_fix="Fix memory leak in connection pooling code",
    )

    known_error.deactivate()

    assert not known_error.is_active()
    assert known_error.status == "INACTIVE"


class TestProblemEvents:
  def test_problem_identified_event(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    events = problem.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ProblemIdentified"

  def test_rca_started_event(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.clear_events()
    problem.start_rca()

    events = problem.get_events()
    assert len(events) == 1
    assert events[0].event_type == "RCAStarted"

  def test_rca_completed_event(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.start_rca()
    problem.clear_events()
    problem.complete_rca("Connection pool exhaustion")

    events = problem.get_events()
    assert len(events) == 1
    assert events[0].event_type == "RCACompleted"

  def test_problem_resolved_event(self):
    problem = Problem(
      problem_id="PROB-001",
      title=Title("Database connection timeout"),
      description=Description("Database connections timing out intermittently"),
      created_by=UserId("user123"),
    )

    problem.clear_events()
    problem.resolve()

    events = problem.get_events()
    assert len(events) == 1
    assert events[0].event_type == "ProblemResolved"
