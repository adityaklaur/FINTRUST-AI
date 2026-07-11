"""Pytest bootstrap: isolate all state under a throwaway temp dir BEFORE the app
is imported, so tests never touch the developer's real DB or vector store.
"""

import os
import pathlib
import tempfile

_tmp = pathlib.Path(tempfile.mkdtemp(prefix="fintrust_test_"))
os.environ.setdefault("SQLITE_PATH", str(_tmp / "test.db"))
os.environ.setdefault("CHROMA_PATH", str(_tmp / "vector_store"))
os.environ.setdefault("LLM_PROVIDER", "none")
os.environ.setdefault("APP_ENV", "test")


def pytest_configure(config):
    # Env above is already set, so the engine points at the temp DB. Create every
    # table (sources + audit_log) up front so no test hits a missing table.
    from app.storage.db import create_db_and_tables

    create_db_and_tables()
