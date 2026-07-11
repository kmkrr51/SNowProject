# ITSM Microservices

Cloud-native ITSM replacement with Domain-Driven Design and microservices architecture.

## Project Structure

```
itsm-microservices/
├── src/
│   ├── shared/              # Shared domain and infrastructure
│   │   ├── domain/          # Core domain models
│   │   └── infrastructure/  # Database, config, event bus
│   ├── incident/            # Incident management service
│   │   ├── domain/          # Domain models
│   │   ├── application/     # Use cases
│   │   ├── infrastructure/  # Repositories
│   │   └── api/             # API endpoints
│   ├── problem/             # Problem management service
│   ├── change/              # Change management service
│   ├── request/             # Request management service
│   └── main.py              # FastAPI application
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
├── Makefile                # Development commands
└── README.md               # This file
```

## Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone repository
cd itsm-microservices

# Install dependencies
make install

# Or manually
pip install -r requirements.txt
```

### Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env as needed
```

## Development

### Run Development Server

```bash
make dev
```

Server will start at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Clean up
make clean
```

## Architecture

### Domain-Driven Design

The application is organized around bounded contexts:

1. **Incident Management** - Incident lifecycle
2. **Problem Management** - Problem identification and RCA
3. **Change Management** - Change requests and approvals
4. **Request Management** - Service request fulfillment

### Layers

- **Domain Layer** - Business logic (entities, aggregates, services)
- **Application Layer** - Use cases (commands, queries, handlers)
- **Infrastructure Layer** - Persistence (repositories, models)
- **API Layer** - External interface (routes, schemas)

### Event-Driven Architecture

Domain events are published by aggregates and handled by event subscribers:

- IncidentCreated
- IncidentAssigned
- IncidentStatusChanged
- IncidentResolved
- IncidentClosed
- SLABreached
- SLAWarning

## API Endpoints

### Health Check

```
GET /health
GET /api/v1/health
```

### Incident Management (Phase 2)

```
POST   /api/v1/incidents
GET    /api/v1/incidents/{id}
GET    /api/v1/incidents
PATCH  /api/v1/incidents/{id}
DELETE /api/v1/incidents/{id}
POST   /api/v1/incidents/{id}/assign
POST   /api/v1/incidents/{id}/resolve
POST   /api/v1/incidents/{id}/close
```

## Development Phases

- **Phase 1** ✅ Foundation & Infrastructure
- **Phase 2** ⏳ Incident Management Service
- **Phase 3** ⏳ Problem Management Service
- **Phase 4** ⏳ Change Management Service
- **Phase 5** ⏳ Request Management Service
- **Phase 6** ⏳ Cross-Cutting Services
- **Phase 7** ⏳ Integration & E2E Testing
- **Phase 8** ⏳ Deployment & Documentation

## Technology Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** SQLite
- **Async:** asyncio, Pydantic
- **Testing:** pytest, pytest-asyncio
- **Code Quality:** Black, Flake8, mypy

## Contributing

1. Follow PEP 8 style guide
2. Use type hints
3. Write tests for new features
4. Run `make format` before committing
5. Ensure `make lint` passes

## License

MIT

## Contact

For questions or issues, please open a GitHub issue.
