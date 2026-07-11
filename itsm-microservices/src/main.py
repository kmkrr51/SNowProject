from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .shared.infrastructure.config import settings
from .incident.api import router as incident_router
from .problem.api import router as problem_router
from .change.api import router as change_router
from .request.api import router as request_router
from .notification.api import router as notification_router
from .search.api import router as search_router
from .audit.api import router as audit_router
try:
  from .auth.api import router as auth_router
except Exception as e:
  print(f"ERROR importing auth router: {e}")
  import traceback
  traceback.print_exc()
  auth_router = None



@asynccontextmanager
async def lifespan(app: FastAPI):
  # Initialize database on startup
  try:
    from .shared.infrastructure import get_database_engine, init_db, close_db
    from pathlib import Path
    import subprocess
    import sys

    engine = await get_database_engine()
    await init_db(engine)

    seed_script = Path(__file__).resolve().parent.parent / "seed_data.py"
    if seed_script.exists():
      subprocess.run([sys.executable, str(seed_script)], check=False, cwd=str(seed_script.parent))

    yield
    await close_db(engine)
  except Exception as e:
    print(f"Database initialization error: {e}")
    print("Starting without database. Using in-memory only.")
    yield


app = FastAPI(
  title=settings.api_title,
  description=settings.api_description,
  version=settings.api_version,
  lifespan=lifespan,
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.allowed_origins,
  allow_credentials=settings.cors_allow_credentials,
  allow_methods=settings.cors_allow_methods,
  allow_headers=settings.cors_allow_headers,
  max_age=settings.cors_max_age,
)

app.include_router(incident_router)
app.include_router(problem_router)
app.include_router(change_router)
app.include_router(request_router)
app.include_router(notification_router)
app.include_router(search_router)
app.include_router(audit_router)
if auth_router:
  app.include_router(auth_router)
else:
  print("WARNING: Auth router not registered due to import error")


@app.get("/health")
async def health_check():
  return {"status": "healthy", "environment": settings.environment}


@app.get("/api/{version}/health")
async def api_health_check(version: str):
  return {
    "status": "healthy",
    "version": version,
    "environment": settings.environment,
  }


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=settings.debug,
  )
