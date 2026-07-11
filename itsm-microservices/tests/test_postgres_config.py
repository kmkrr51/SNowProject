import os

from src.shared.infrastructure.config import Settings


def test_settings_default_database_url_uses_postgresql(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    settings = Settings(_env_file=None)

    assert settings.database_url.startswith("postgresql+asyncpg://")
