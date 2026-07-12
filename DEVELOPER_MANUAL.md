# SNowProject - Developer Manual: Incident Use Case

## Overview
This manual provides a high-level guide for developers working on the Incident feature. It maps common changes to the specific files that need modification.

---

## Architecture Overview

### Incident Flow
```
Frontend Form → API Request → Backend Handler → Database → Response → Frontend Display
```

### Key Components
1. **Frontend**: React components + Redux state management
2. **Backend**: FastAPI routes + Domain-driven design handlers
3. **Database**: PostgreSQL with SQLAlchemy ORM

---

## Common Changes & File Locations

### 1. Adding a New Incident Field

#### Scenario: Add "severity_level" field to incidents

**Files to Modify**:

1. **Database Schema** (`itsm-microservices/src/incident/infrastructure/models.py`)
   - Add column: `severity_level: Column(String)`
   - Example:
   ```python
   severity_level: Mapped[str] = mapped_column(String(50))
   ```

2. **Domain Model** (`itsm-microservices/src/incident/domain/incident.py`)
   - Add field to Incident class
   - Example:
   ```python
   severity_level: SeverityLevel
   ```

3. **API Schema** (`itsm-microservices/src/incident/api/schemas.py`)
   - Add to CreateIncidentRequest:
   ```python
   severity_level: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
   ```
   - Add to IncidentResponse:
   ```python
   severity_level: str
   ```

4. **Frontend Type** (`frontend/src/types/incident.types.ts`)
   - Add to Incident interface:
   ```typescript
   severityLevel: string;
   ```

5. **Frontend Form** (`frontend/src/components/incident/CreateIncidentModal.tsx`)
   - Add form field and state
   - Add to formData object

---

### 2. Changing Incident Status Workflow

#### Scenario: Add new status "ESCALATED"

**Files to Modify**:

1. **Domain Enum** (`itsm-microservices/src/shared/domain/value_objects.py`)
   - Update Status enum:
   ```python
   class Status(str, Enum):
     NEW = "NEW"
     ASSIGNED = "ASSIGNED"
     IN_PROGRESS = "IN_PROGRESS"
     ESCALATED = "ESCALATED"  # Add this
     RESOLVED = "RESOLVED"
     CLOSED = "CLOSED"
   ```

2. **API Schema** (`itsm-microservices/src/incident/api/schemas.py`)
   - Update ChangeStatusRequest description:
   ```python
   new_status: str = Field(..., description="NEW, ASSIGNED, IN_PROGRESS, ESCALATED, RESOLVED, CLOSED")
   ```

3. **Frontend Types** (`frontend/src/types/incident.types.ts`)
   - Update IncidentStatus type:
   ```typescript
   type IncidentStatus = "NEW" | "ASSIGNED" | "IN_PROGRESS" | "ESCALATED" | "RESOLVED" | "CLOSED";
   ```

4. **Frontend Component** (`frontend/src/components/incident/IncidentList.tsx`)
   - Update status dropdown/filter options

---

### 3. Adding a New Incident Action (e.g., "Escalate")

#### Scenario: Add escalate incident endpoint

**Files to Modify**:

1. **Command** (`itsm-microservices/src/incident/application/commands.py`)
   - Add new command:
   ```python
   @dataclass
   class EscalateIncidentCommand:
     incident_id: str
     escalation_reason: str
   ```

2. **Handler** (`itsm-microservices/src/incident/application/handlers.py`)
   - Add handler class:
   ```python
   class EscalateIncidentHandler:
     def __init__(self, repository: IncidentRepository):
       self.repository = repository
     
     async def handle(self, command: EscalateIncidentCommand) -> str:
       # Implementation
   ```

3. **Dependency** (`itsm-microservices/src/incident/api/dependencies.py`)
   - Add dependency function:
   ```python
   async def get_escalate_incident_handler(repository: IncidentRepository = None) -> EscalateIncidentHandler:
     if repository is None:
       async for repo in get_incident_repository():
         return EscalateIncidentHandler(repo)
     return EscalateIncidentHandler(repository)
   ```

4. **Route** (`itsm-microservices/src/incident/api/routes.py`)
   - Add endpoint:
   ```python
   @router.post("/{incident_id}/escalate", status_code=200)
   async def escalate_incident(incident_id: str, request: EscalateRequest, session: AsyncSession = Depends(get_session)):
     # Implementation
   ```

5. **Frontend Service** (`frontend/src/services/incident.service.ts`)
   - Add method:
   ```typescript
   escalateIncident: async (id: string, reason: string): Promise<Incident> => {
     const response = await apiClient.post(`/incidents/${id}/escalate`, { reason });
     return response.data;
   }
   ```

6. **Frontend Thunk** (`frontend/src/store/thunks/incidentThunks.ts`)
   - Add thunk for async action

7. **Frontend Component** (`frontend/src/components/incident/IncidentList.tsx`)
   - Add button/action to trigger escalation

---

### 4. Modifying Incident List Filters

#### Scenario: Add severity_level filter to incident list

**Files to Modify**:

1. **Query** (`itsm-microservices/src/incident/application/queries.py`)
   - Update ListIncidentsQuery:
   ```python
   @dataclass
   class ListIncidentsQuery:
     status: Optional[str] = None
     priority: Optional[str] = None
     severity_level: Optional[str] = None  # Add this
     assigned_to: Optional[str] = None
     limit: int = 100
     offset: int = 0
   ```

2. **Handler** (`itsm-microservices/src/incident/application/handlers.py`)
   - Update ListIncidentsQueryHandler.handle() to filter by severity_level

3. **Route** (`itsm-microservices/src/incident/api/routes.py`)
   - Add query parameter:
   ```python
   severity_level: Optional[str] = Query(None)
   ```

4. **Frontend Component** (`frontend/src/components/incident/IncidentList.tsx`)
   - Add filter dropdown for severity_level
   - Update table columns if needed

---

### 5. Changing Date/Time Display Format

#### Scenario: Change date format from "Jul 12, 2026" to "2026-07-12"

**Files to Modify**:

1. **Frontend Utility** (`frontend/src/utils/dateFormatter.ts`)
   - Update formatDate function:
   ```typescript
   return date.toLocaleDateString("en-US", {
     year: "numeric",
     month: "2-digit",
     day: "2-digit",
   });
   ```

2. **All Components Using Dates**:
   - `frontend/src/components/incident/IncidentList.tsx` (already uses formatDate)
   - No other changes needed if using formatDate utility

---

### 6. Adding Incident Validation

#### Scenario: Validate incident title is at least 10 characters

**Files to Modify**:

1. **API Schema** (`itsm-microservices/src/incident/api/schemas.py`)
   - Update CreateIncidentRequest:
   ```python
   title: str = Field(..., min_length=10, max_length=255)
   ```

2. **Frontend Validation** (`frontend/src/components/incident/CreateIncidentModal.tsx`)
   - Add client-side validation:
   ```typescript
   if (formData.title.length < 10) {
     // Show error
   }
   ```

---

### 7. Modifying Incident Response Data

#### Scenario: Add incident resolution time to response

**Files to Modify**:

1. **API Schema** (`itsm-microservices/src/incident/api/schemas.py`)
   - Add to IncidentResponse:
   ```python
   resolution_time_minutes: Optional[int] = None
   ```

2. **Domain Model** (`itsm-microservices/src/incident/domain/incident.py`)
   - Add property or method to calculate resolution time

3. **Route** (`itsm-microservices/src/incident/api/routes.py`)
   - Calculate and populate field in response mapping

4. **Frontend Type** (`frontend/src/types/incident.types.ts`)
   - Add to Incident interface:
   ```typescript
   resolutionTimeMinutes?: number;
   ```

5. **Frontend Component** (`frontend/src/components/incident/IncidentList.tsx`)
   - Add column to display resolution time

---

### 8. Changing Incident Sorting

#### Scenario: Sort incidents by priority and created_at

**Files to Modify**:

1. **Handler** (`itsm-microservices/src/incident/application/handlers.py`)
   - Update ListIncidentsQueryHandler.handle():
   ```python
   incidents = sorted(incidents, key=lambda x: (x.priority.value, x.created_at.value), reverse=True)
   ```

2. **Frontend Component** (`frontend/src/components/incident/IncidentList.tsx`)
   - Update table column sorter configuration

---

### 9. Adding Incident Pagination

#### Scenario: Implement pagination for incident list

**Files to Modify**:

1. **Query** (`itsm-microservices/src/incident/application/queries.py`)
   - Already has limit and offset

2. **Route** (`itsm-microservices/src/incident/api/routes.py`)
   - Already implements pagination

3. **Frontend Component** (`frontend/src/components/incident/IncidentList.tsx`)
   - Add pagination controls
   - Update thunk call with offset/limit parameters

---

### 10. Changing Incident Error Handling

#### Scenario: Add custom error message for duplicate incident

**Files to Modify**:

1. **Handler** (`itsm-microservices/src/incident/application/handlers.py`)
   - Add validation in CreateIncidentHandler.handle():
   ```python
   existing = await self.repository.find_by_title(command.title)
   if existing:
     raise ValueError("Incident with this title already exists")
   ```

2. **Route** (`itsm-microservices/src/incident/api/routes.py`)
   - Error handling already in place, will catch ValueError

3. **Frontend** (`frontend/src/components/incident/CreateIncidentModal.tsx`)
   - Display error message from backend response

---

## Database Queries Reference

### Common Incident Queries

**Get all incidents**:
```python
await repository.find_all()
```

**Get incident by ID**:
```python
await repository.find_by_id(incident_id)
```

**Get incidents by status**:
```python
incidents = [i for i in all_incidents if i.status.value == status]
```

**Get incidents by priority**:
```python
incidents = [i for i in all_incidents if i.priority.value == priority]
```

---

## API Endpoints Reference

### Incident Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/incidents` | Create incident |
| GET | `/api/v1/incidents` | List incidents |
| GET | `/api/v1/incidents/{id}` | Get incident by ID |
| PATCH | `/api/v1/incidents/{id}` | Update incident |
| POST | `/api/v1/incidents/{id}/assign` | Assign incident |
| POST | `/api/v1/incidents/{id}/change-status` | Change status |
| POST | `/api/v1/incidents/{id}/resolve` | Resolve incident |
| POST | `/api/v1/incidents/{id}/close` | Close incident |

---

## Testing Changes

### Backend Testing
```bash
cd itsm-microservices
python -m pytest tests/incident/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing
1. Start backend: `python -m uvicorn src.main:app --reload`
2. Start frontend: `npm run dev`
3. Test in browser at `http://localhost:3001`

---

## Git Workflow

### Commit Pattern
```
[backend] Brief description of change
[frontend] Brief description of change
[docs] Documentation updates
```

### Example
```bash
git add .
git commit -m "[backend] Add severity_level field to incidents"
git push origin main
```

---

## Key Files Quick Reference

| Purpose | File Path |
|---------|-----------|
| Domain Model | `itsm-microservices/src/incident/domain/incident.py` |
| Database Model | `itsm-microservices/src/incident/infrastructure/models.py` |
| API Routes | `itsm-microservices/src/incident/api/routes.py` |
| API Schemas | `itsm-microservices/src/incident/api/schemas.py` |
| Handlers | `itsm-microservices/src/incident/application/handlers.py` |
| Commands | `itsm-microservices/src/incident/application/commands.py` |
| Queries | `itsm-microservices/src/incident/application/queries.py` |
| Frontend Types | `frontend/src/types/incident.types.ts` |
| Frontend Service | `frontend/src/services/incident.service.ts` |
| Frontend Thunks | `frontend/src/store/thunks/incidentThunks.ts` |
| Frontend Slice | `frontend/src/store/slices/incidentSlice.ts` |
| Frontend Component | `frontend/src/components/incident/IncidentList.tsx` |
| Create Modal | `frontend/src/components/incident/CreateIncidentModal.tsx` |

---

## Important Notes

1. **Always update both backend and frontend** when adding fields
2. **Use camelCase in frontend**, snake_case in backend
3. **Add aliases in Pydantic schemas** for field name conversion
4. **Test date handling** - use ISO 8601 format
5. **Check for duplicates** in seed data before inserting
6. **Add error logging** to HTTP exception handlers
7. **Use formatDate utility** for all date displays in frontend

---

## Common Pitfalls

❌ **Don't**: Forget to add field to both frontend and backend
✅ **Do**: Update type definitions, schemas, and components together

❌ **Don't**: Use different field names in frontend and backend
✅ **Do**: Use aliases in Pydantic to handle naming differences

❌ **Don't**: Return raw datetime objects from API
✅ **Do**: Use json_encoders to serialize to ISO format

❌ **Don't**: Hardcode date formats in components
✅ **Do**: Use formatDate utility function

---

## Support & Questions

For questions about incident implementation:
1. Check CHAT_HISTORY.md for session notes
2. Review existing handlers for patterns
3. Check API schema for field definitions
4. Test with curl or Postman before frontend integration

---

**Last Updated**: July 12, 2026
**Scope**: Incident Use Case Only
