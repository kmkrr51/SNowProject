import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.shared.infrastructure.database import Base
from src.incident.infrastructure.models import IncidentModel, TechnicianModel, WorkNoteModel, SLAModel
from src.problem.infrastructure.models import ProblemModel, RCARecordModel, KnownErrorModel
from src.change.infrastructure.models import ChangeRequestModel
from src.request.infrastructure.models import ServiceRequestModel
from src.notification.infrastructure.models import NotificationModel
from src.search.infrastructure.models import SearchIndexModel
from src.audit.infrastructure.models import AuditLogModel


async def seed_database():
  from src.shared.infrastructure.config import settings

  engine = create_async_engine(settings.database_url, echo=False)

  async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  async with async_session() as session:
    print("[*] Seeding database with test data...")

    existing_techs = {tech.id for tech in (await session.execute(__import__('sqlalchemy').select(TechnicianModel))).scalars().all()}
    technicians = [
      TechnicianModel(
        id="tech_001",
        name="John Smith",
        skills="Network, Infrastructure, Cloud",
        availability="AVAILABLE",
        current_workload=3,
        historical_resolution_rate=95,
      ),
      TechnicianModel(
        id="tech_002",
        name="Sarah Johnson",
        skills="Database, Performance, Security",
        availability="AVAILABLE",
        current_workload=2,
        historical_resolution_rate=98,
      ),
      TechnicianModel(
        id="tech_003",
        name="Mike Davis",
        skills="Application, API, Integration",
        availability="BUSY",
        current_workload=5,
        historical_resolution_rate=92,
      ),
    ]
    for technician in technicians:
      if technician.id not in existing_techs:
        session.add(technician)
    await session.flush()
    print("[OK] Ensured 3 technicians")

    existing_slas = {sla.id for sla in (await session.execute(__import__('sqlalchemy').select(SLAModel))).scalars().all()}
    slas = [
      SLAModel(
        id="sla_001",
        name="Critical SLA",
        priority="CRITICAL",
        response_time_hours=1,
        response_time_minutes=0,
        resolution_time_hours=4,
        resolution_time_minutes=0,
      ),
      SLAModel(
        id="sla_002",
        name="High SLA",
        priority="HIGH",
        response_time_hours=2,
        response_time_minutes=0,
        resolution_time_hours=8,
        resolution_time_minutes=0,
      ),
      SLAModel(
        id="sla_003",
        name="Medium SLA",
        priority="MEDIUM",
        response_time_hours=4,
        response_time_minutes=0,
        resolution_time_hours=24,
        resolution_time_minutes=0,
      ),
    ]
    for sla in slas:
      if sla.id not in existing_slas:
        session.add(sla)
    await session.flush()
    print("[OK] Ensured 3 SLAs")

    existing_incidents = {inc.id for inc in (await session.execute(__import__('sqlalchemy').select(IncidentModel))).scalars().all()}
    incidents = [
      IncidentModel(
        id="inc_001",
        title="Database Connection Timeout",
        description="Production database is experiencing connection timeouts affecting all users",
        priority="CRITICAL",
        status="ASSIGNED",
        impact_level="HIGH",
        urgency_level="HIGH",
        assigned_to="tech_001",
        created_by="user_001",
        created_at=datetime.utcnow() - timedelta(hours=2),
      ),
      IncidentModel(
        id="inc_002",
        title="API Response Time Degradation",
        description="API endpoints are responding slower than normal",
        priority="HIGH",
        status="ASSIGNED",
        impact_level="MEDIUM",
        urgency_level="HIGH",
        assigned_to="tech_002",
        created_by="user_002",
        created_at=datetime.utcnow() - timedelta(hours=1),
      ),
      IncidentModel(
        id="inc_003",
        title="Email Service Down",
        description="Email notifications are not being sent",
        priority="HIGH",
        status="NEW",
        impact_level="MEDIUM",
        urgency_level="MEDIUM",
        assigned_to=None,
        created_by="user_003",
        created_at=datetime.utcnow() - timedelta(minutes=30),
      ),
      IncidentModel(
        id="inc_004",
        title="Dashboard Widget Error",
        description="Dashboard widget is showing error message",
        priority="MEDIUM",
        status="RESOLVED",
        impact_level="LOW",
        urgency_level="LOW",
        assigned_to="tech_003",
        created_by="user_001",
        created_at=datetime.utcnow() - timedelta(days=1),
        resolved_at=datetime.utcnow() - timedelta(hours=12),
      ),
      IncidentModel(
        id="inc_005",
        title="Login Page Slow",
        description="Login page takes too long to load",
        priority="MEDIUM",
        status="CLOSED",
        impact_level="LOW",
        urgency_level="MEDIUM",
        assigned_to="tech_001",
        created_by="user_002",
        created_at=datetime.utcnow() - timedelta(days=2),
        resolved_at=datetime.utcnow() - timedelta(days=1, hours=12),
        closed_at=datetime.utcnow() - timedelta(days=1),
      ),
    ]
    for incident in incidents:
      if incident.id not in existing_incidents:
        session.add(incident)
    await session.flush()
    print("[OK] Ensured 5 incidents")

    work_notes = [
      WorkNoteModel(
        id="note_001",
        incident_id="inc_001",
        technician_id="tech_001",
        content="Investigating database connection pool settings",
      ),
      WorkNoteModel(
        id="note_002",
        incident_id="inc_001",
        technician_id="tech_001",
        content="Found connection leak in application code",
      ),
      WorkNoteModel(
        id="note_003",
        incident_id="inc_002",
        technician_id="tech_002",
        content="Checking database query performance",
      ),
    ]
    session.add_all(work_notes)
    await session.flush()
    print("[OK] Created 3 work notes")

    problems = [
      ProblemModel(
        id="prob_001",
        title="Recurring Database Timeout Issue",
        description="Database connections are timing out intermittently",
        status="INVESTIGATING",
        root_cause="Connection pool exhaustion due to slow queries",
        created_by="user_001",
        created_at=datetime.utcnow() - timedelta(days=3),
        related_incidents="inc_001, inc_002",
        impacted_services="API, Web Portal",
      ),
      ProblemModel(
        id="prob_002",
        title="Memory Leak in Background Service",
        description="Background service is consuming increasing memory",
        status="RESOLVED",
        root_cause="Event listener not being properly cleaned up",
        created_by="user_002",
        created_at=datetime.utcnow() - timedelta(days=5),
        resolved_at=datetime.utcnow() - timedelta(days=1),
        related_incidents="inc_003",
        impacted_services="Notification Service",
      ),
      ProblemModel(
        id="prob_003",
        title="Cache Invalidation Issue",
        description="Cache is not being invalidated properly",
        status="NEW",
        root_cause=None,
        created_by="user_003",
        created_at=datetime.utcnow() - timedelta(hours=6),
        related_incidents="inc_004",
        impacted_services="Dashboard",
      ),
    ]
    session.add_all(problems)
    await session.flush()
    print("[OK] Created 3 problems")

    rca_records = [
      RCARecordModel(
        id="rca_001",
        problem_id="prob_001",
        analysis_details="Root cause analysis shows connection pool misconfiguration",
        contributing_factors="High query volume, slow database response",
        timeline="Issue started after database upgrade",
      ),
      RCARecordModel(
        id="rca_002",
        problem_id="prob_002",
        analysis_details="Memory leak found in event listener cleanup",
        contributing_factors="Improper resource disposal in async operations",
        timeline="Gradual memory increase over 2 weeks",
      ),
    ]
    session.add_all(rca_records)
    await session.flush()
    print("[OK] Created 2 RCA records")

    known_errors = [
      KnownErrorModel(
        id="ke_001",
        problem_id="prob_001",
        workaround="Restart the application service",
        temporary_fix="Increase connection pool size temporarily",
        permanent_fix="Optimize slow queries and implement connection pooling",
        status="ACTIVE",
      ),
      KnownErrorModel(
        id="ke_002",
        problem_id="prob_002",
        workaround="Restart background service daily",
        temporary_fix="Monitor memory usage and restart when threshold reached",
        permanent_fix="Fix event listener cleanup in service code",
        status="RESOLVED",
      ),
    ]
    session.add_all(known_errors)
    await session.flush()
    print("[OK] Created 2 known errors")

    changes = [
      ChangeRequestModel(
        id="chg_001",
        title="Database Connection Pool Optimization",
        description="Optimize database connection pool settings",
        change_type="CONFIGURATION",
        status="SUBMITTED",
        risk_level="MEDIUM",
        impact_assessment="Will improve application performance",
        rollback_plan="Revert to previous connection pool settings",
        implementation_schedule=datetime.utcnow() + timedelta(days=3),
        created_by="user_001",
        created_at=datetime.utcnow() - timedelta(days=1),
        approvals="manager_001, tech_lead_001",
      ),
      ChangeRequestModel(
        id="chg_002",
        title="Upgrade Node.js Runtime",
        description="Upgrade Node.js to latest LTS version",
        change_type="INFRASTRUCTURE",
        status="APPROVED",
        risk_level="LOW",
        impact_assessment="Performance improvement and security patches",
        rollback_plan="Rollback to previous Node.js version",
        implementation_schedule=datetime.utcnow() + timedelta(days=7),
        created_by="user_002",
        created_at=datetime.utcnow() - timedelta(days=2),
        approvals="manager_001",
      ),
      ChangeRequestModel(
        id="chg_003",
        title="Add New API Endpoint",
        description="Add new endpoint for user preferences",
        change_type="DEVELOPMENT",
        status="IMPLEMENTED",
        risk_level="LOW",
        impact_assessment="New functionality for users",
        rollback_plan="Remove new endpoint and revert code",
        implementation_schedule=datetime.utcnow() - timedelta(days=1),
        created_by="user_003",
        created_at=datetime.utcnow() - timedelta(days=5),
        implemented_at=datetime.utcnow() - timedelta(days=1),
        approvals="manager_001, tech_lead_001",
      ),
    ]
    session.add_all(changes)
    await session.flush()
    print("[OK] Created 3 change requests")

    requests = [
      ServiceRequestModel(
        id="req_001",
        request_type="ACCESS_REQUEST",
        title="Request Access to Production Database",
        description="Need read-only access to production database for reporting",
        status="PENDING",
        requester="user_004",
        requested_service="Database Access",
        priority="HIGH",
        assigned_to="tech_001",
        fulfillment_details="Pending approval from database administrator",
        created_at=datetime.utcnow() - timedelta(hours=4),
      ),
      ServiceRequestModel(
        id="req_002",
        request_type="SOFTWARE_REQUEST",
        title="Request New Monitoring Tool License",
        description="Need license for advanced monitoring tool",
        status="PENDING",
        requester="user_005",
        requested_service="Monitoring Tool",
        priority="MEDIUM",
        assigned_to="tech_002",
        fulfillment_details="Waiting for budget approval",
        created_at=datetime.utcnow() - timedelta(hours=8),
      ),
      ServiceRequestModel(
        id="req_003",
        request_type="HARDWARE_REQUEST",
        title="Request New Laptop",
        description="Need new laptop for development",
        status="FULFILLED",
        requester="user_006",
        requested_service="Hardware",
        priority="MEDIUM",
        assigned_to="tech_003",
        fulfillment_details="Laptop ordered and will be delivered next week",
        fulfilled_at=datetime.utcnow() - timedelta(hours=2),
        created_at=datetime.utcnow() - timedelta(days=1),
      ),
      ServiceRequestModel(
        id="req_004",
        request_type="INFORMATION_REQUEST",
        title="Request System Documentation",
        description="Need documentation for system architecture",
        status="CLOSED",
        requester="user_007",
        requested_service="Documentation",
        priority="LOW",
        assigned_to="tech_001",
        fulfillment_details="Documentation provided via email",
        fulfilled_at=datetime.utcnow() - timedelta(days=2),
        closed_at=datetime.utcnow() - timedelta(days=1),
        created_at=datetime.utcnow() - timedelta(days=3),
      ),
    ]
    session.add_all(requests)
    await session.flush()
    print("[OK] Created 4 service requests")

    notifications = [
      NotificationModel(
        id="notif_001",
        recipient_id="user_001",
        subject="Incident Assigned",
        message="You have been assigned to incident INC_001",
        notification_type="INCIDENT",
        related_entity_id="inc_001",
        related_entity_type="INCIDENT",
        status="UNREAD",
        created_at=datetime.utcnow() - timedelta(minutes=15),
      ),
      NotificationModel(
        id="notif_002",
        recipient_id="user_002",
        subject="Change Approved",
        message="Your change request CHG_002 has been approved",
        notification_type="CHANGE",
        related_entity_id="chg_002",
        related_entity_type="CHANGE",
        status="READ",
        created_at=datetime.utcnow() - timedelta(hours=1),
        read_at=datetime.utcnow() - timedelta(minutes=30),
      ),
      NotificationModel(
        id="notif_003",
        recipient_id="user_003",
        subject="Problem Created",
        message="New problem PROB_003 has been created",
        notification_type="PROBLEM",
        related_entity_id="prob_003",
        related_entity_type="PROBLEM",
        status="UNREAD",
        created_at=datetime.utcnow() - timedelta(hours=6),
      ),
      NotificationModel(
        id="notif_004",
        recipient_id="user_004",
        subject="Request Status Update",
        message="Your service request REQ_001 is pending approval",
        notification_type="REQUEST",
        related_entity_id="req_001",
        related_entity_type="REQUEST",
        status="READ",
        created_at=datetime.utcnow() - timedelta(hours=3),
        read_at=datetime.utcnow() - timedelta(hours=2),
      ),
    ]
    session.add_all(notifications)
    await session.flush()
    print("[OK] Created 4 notifications")

    search_indexes = [
      SearchIndexModel(
        id="search_001",
        entity_id="inc_001",
        entity_type="INCIDENT",
        title="Database Connection Timeout",
        description="Production database is experiencing connection timeouts",
        content="Database Connection Timeout Production database is experiencing connection timeouts affecting all users",
        search_metadata='{"priority": "CRITICAL", "status": "ASSIGNED"}',
      ),
      SearchIndexModel(
        id="search_002",
        entity_id="prob_001",
        entity_type="PROBLEM",
        title="Recurring Database Timeout Issue",
        description="Database connections are timing out intermittently",
        content="Recurring Database Timeout Issue Database connections are timing out intermittently",
        search_metadata='{"status": "INVESTIGATING"}',
      ),
      SearchIndexModel(
        id="search_003",
        entity_id="chg_001",
        entity_type="CHANGE",
        title="Database Connection Pool Optimization",
        description="Optimize database connection pool settings",
        content="Database Connection Pool Optimization Optimize database connection pool settings",
        search_metadata='{"status": "SUBMITTED", "risk_level": "MEDIUM"}',
      ),
      SearchIndexModel(
        id="search_004",
        entity_id="req_001",
        entity_type="REQUEST",
        title="Request Access to Production Database",
        description="Need read-only access to production database for reporting",
        content="Request Access to Production Database Need read-only access to production database for reporting",
        search_metadata='{"status": "PENDING", "priority": "HIGH"}',
      ),
    ]
    session.add_all(search_indexes)
    await session.flush()
    print("[OK] Created 4 search indexes")

    audit_logs = [
      AuditLogModel(
        id="audit_001",
        entity_id="inc_001",
        entity_type="INCIDENT",
        action="CREATE",
        actor_id="user_001",
        changes='{"title": "Database Connection Timeout", "priority": "CRITICAL"}',
        created_at=datetime.utcnow() - timedelta(hours=2),
      ),
      AuditLogModel(
        id="audit_002",
        entity_id="inc_001",
        entity_type="INCIDENT",
        action="UPDATE",
        actor_id="tech_001",
        changes='{"status": "ASSIGNED", "assigned_to": "tech_001"}',
        created_at=datetime.utcnow() - timedelta(hours=1, minutes=45),
      ),
      AuditLogModel(
        id="audit_003",
        entity_id="prob_001",
        entity_type="PROBLEM",
        action="CREATE",
        actor_id="user_001",
        changes='{"title": "Recurring Database Timeout Issue", "status": "INVESTIGATING"}',
        created_at=datetime.utcnow() - timedelta(days=3),
      ),
      AuditLogModel(
        id="audit_004",
        entity_id="chg_001",
        entity_type="CHANGE",
        action="CREATE",
        actor_id="user_001",
        changes='{"title": "Database Connection Pool Optimization", "status": "SUBMITTED"}',
        created_at=datetime.utcnow() - timedelta(days=1),
      ),
      AuditLogModel(
        id="audit_005",
        entity_id="chg_002",
        entity_type="CHANGE",
        action="UPDATE",
        actor_id="manager_001",
        changes='{"status": "APPROVED"}',
        created_at=datetime.utcnow() - timedelta(days=1, hours=12),
      ),
      AuditLogModel(
        id="audit_006",
        entity_id="req_001",
        entity_type="REQUEST",
        action="CREATE",
        actor_id="user_004",
        changes='{"title": "Request Access to Production Database", "status": "PENDING"}',
        created_at=datetime.utcnow() - timedelta(hours=4),
      ),
    ]
    session.add_all(audit_logs)
    await session.flush()
    print("[OK] Created 6 audit logs")

    await session.commit()
    print("\n[SUCCESS] Database seeding completed successfully!")
    print("\n[SUMMARY] Summary:")
    print("  - 3 Technicians")
    print("  - 3 SLAs")
    print("  - 5 Incidents")
    print("  - 3 Work Notes")
    print("  - 3 Problems")
    print("  - 2 RCA Records")
    print("  - 2 Known Errors")
    print("  - 3 Change Requests")
    print("  - 4 Service Requests")
    print("  - 4 Notifications")
    print("  - 4 Search Indexes")
    print("  - 6 Audit Logs")

  await engine.dispose()


if __name__ == "__main__":
  asyncio.run(seed_database())
