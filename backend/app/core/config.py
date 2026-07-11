"""Central configuration.

All runtime knobs live here and are read from environment variables (or a
`.env` file next to this backend). Every field has a safe default so the app
boots with an empty environment — the only thing you *may* want to set is an
LLM provider + key, and even that is optional (see ``llm_provider="none"``).

Design note: paths are resolved relative to the backend directory, not the
current working directory, so `uvicorn`, `pytest`, and the CLI scripts all
agree on where the database and vector store live regardless of where you
launch them from.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# .../backend/app/core/config.py -> parents[2] == .../backend
BACKEND_DIR: Path = Path(__file__).resolve().parents[2]
PROJECT_ROOT: Path = BACKEND_DIR.parent
DATA_DIR: Path = BACKEND_DIR / "data"
SOURCES_DIR: Path = PROJECT_ROOT / "sources"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- General ---
    app_env: str = "local"
    log_level: str = "INFO"

    # --- LLM (generation) ---
    # Provider is swappable without code changes. "none" uses a fully offline
    # extractive answerer so the app works with zero API keys.
    llm_provider: str = Field(
        default="none", description="none | groq | gemini | openai | anthropic"
    )
    llm_api_key: str = ""
    llm_model: str = ""  # empty => provider-specific default chosen in llm_client
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1200

    # Optional automatic fallback provider (tried only if the primary errors / is
    # rate-limited). Leave blank to disable. Example: primary=groq, fallback=gemini.
    llm_fallback_provider: str = ""
    llm_fallback_api_key: str = ""
    llm_fallback_model: str = ""

    # --- Embeddings + vector store ---
    embedding_model: str = "all-MiniLM-L6-v2"
    collection_name: str = "fintrust_v1"
    chroma_path: str = ""  # empty => DATA_DIR/vector_store

    # --- Relational storage ---
    sqlite_path: str = ""  # empty => DATA_DIR/fintrust.db
    # Full SQLAlchemy DB URL (e.g. postgresql+psycopg://user:pwd@host/db). Blank =>
    # the local SQLite file above. Point this at Supabase/Neon Postgres in prod.
    database_url: str = ""

    # --- Auth (optional; Supabase). Blank secret => anonymous mode, no login. ---
    supabase_jwt_secret: str = ""

    # --- Retrieval tuning ---
    retrieval_top_k: int = 8
    min_chunk_score: float = 0.25  # drop chunks below this similarity
    refusal_score: float = 0.35  # if best chunk < this => refuse, don't hallucinate

    # --- Chunking (all in estimated tokens; tune without code changes) ---
    # 384 gives finer, more precisely-retrievable chunks for FAQ/clause text.
    chunk_target_tokens: int = 384
    chunk_overlap_tokens: int = 64
    chunk_hard_max_tokens: int = 576
    chunk_min_tokens: int = 64

    # --- Document refresh (staying current WITHOUT training) ---
    rbi_rss_url: str = "https://www.rbi.org.in/notifications_rss.xml"
    refresh_timeout_seconds: int = 30
    refresh_user_agent: str = "FinTrustAI/0.1 (document-refresh)"

    # --- CORS (comma-separated origins) ---
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # ------------------------------------------------------------------ #
    # Derived helpers
    # ------------------------------------------------------------------ #
    @property
    def chroma_dir(self) -> Path:
        return Path(self.chroma_path) if self.chroma_path else DATA_DIR / "vector_store"

    @property
    def sqlite_file(self) -> Path:
        return Path(self.sqlite_path) if self.sqlite_path else DATA_DIR / "fintrust.db"

    @property
    def sqlite_url(self) -> str:
        return f"sqlite:///{self.sqlite_file}"

    @property
    def db_url(self) -> str:
        return self.database_url or self.sqlite_url

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def ensure_dirs(self) -> None:
        """Create data directories so nothing downstream has to guard for them."""
        for path in (DATA_DIR, self.chroma_dir, DATA_DIR / "eval", DATA_DIR / "audit"):
            path.mkdir(parents=True, exist_ok=True)
        self.sqlite_file.parent.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings
