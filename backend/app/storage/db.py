"""SQLite / Postgres engine + table lifecycle via SQLModel.

Uses ``settings.db_url`` — SQLite by default, or a Postgres URL (Supabase/Neon)
when ``DATABASE_URL`` is set. A tiny idempotent migration adds columns that were
introduced after a table already existed (so upgrading doesn't require a wipe).
"""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

_settings = get_settings()
_is_sqlite = _settings.db_url.startswith("sqlite")

# check_same_thread=False is a SQLite-only concern (FastAPI serves across threads).
engine = create_engine(
    _settings.db_url,
    echo=False,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
)


def create_db_and_tables() -> None:
    # Import models for their side effect of registering with SQLModel.metadata.
    from app.schemas import audit as _audit  # noqa: F401
    from app.schemas import source as _source  # noqa: F401

    SQLModel.metadata.create_all(engine)
    _run_light_migrations()


def _run_light_migrations() -> None:
    """Add columns introduced after a table already existed. Each statement runs
    in its own transaction so an 'already exists' error doesn't poison the rest."""
    migrations = [
        "ALTER TABLE audit_log ADD COLUMN user_id VARCHAR DEFAULT 'anonymous'",
    ]
    for stmt in migrations:
        try:
            with engine.begin() as conn:
                conn.execute(text(stmt))
        except Exception:  # noqa: BLE001 - column already present is expected
            pass


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
