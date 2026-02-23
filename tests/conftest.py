"""
conftest.py — shared pytest fixtures.

ROOT CAUSE: `app/core/settings.py` calls `load_dotenv('.env', override=True)` at
module-level. This forces the remote MONGODB_URL from .env into the environment,
and `pymongo.MongoClient` then blocks on DNS/TCP resolution to that host.

FIX (applied before ANY app code is imported):
  1. Patch `dotenv.load_dotenv` → no-op (prevents .env from overriding MONGODB_URL)
  2. Set MONGODB_URL in os.environ to a safe local value
  3. Patch `pymongo.MongoClient` → MagicMock (belt-and-suspenders, prevents TCP)
  4. Override the FastAPI lifespan → no-op (TestClient won't run startup hooks)
  5. Inject MagicMock UseCases via dependency_overrides (no real DB ever accessed)
"""
import os
import pytest
from contextlib import asynccontextmanager
from unittest.mock import MagicMock, patch

# ── 1. Prevent .env from loading (it contains a remote MONGODB_URL) ───────────
_dotenv_patch = patch("dotenv.load_dotenv", return_value=None)
_dotenv_patch.start()

# ── 2. Set a safe local MONGODB_URL ──────────────────────────────────────────
os.environ["MONGODB_URL"] = "mongodb://localhost:27017"

# ── 3. Patch pymongo.MongoClient so no TCP socket is ever opened ──────────────
_mongo_patch = patch("pymongo.MongoClient", new=MagicMock)
_mongo_patch.start()

# ── 4. No-op lifespan ─────────────────────────────────────────────────────────
@asynccontextmanager
async def _noop_lifespan(app):
    yield


# ── 5. Import the FastAPI app AFTER all patches ───────────────────────────────
from fastapi.testclient import TestClient   # noqa: E402
from app.api.server import app             # noqa: E402

app.router.lifespan_context = _noop_lifespan

# ── 6. Dependency functions to override ───────────────────────────────────────
from app.api.dependencies.use_cases.agents import (  # noqa: E402
    get_create_agent_use_case,
    get_list_agents_use_case,
    delete_agents_use_case,
)
from app.api.dependencies.use_cases.tools import (  # noqa: E402
    get_create_tool_use_case,
    get_list_tools_use_case,
    delete_tools_use_case as get_delete_tools_use_case,
)
from app.api.dependencies.use_cases.knowledge_bases import (  # noqa: E402
    get_create_knowledge_base_use_case,
    get_list_knowledge_bases_use_case,
    delete_knowledge_bases_use_case as get_delete_knowledge_bases_use_case,
)


# ── 7. Session-scoped TestClient with all use cases mocked ────────────────────
@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    FastAPI TestClient with all Use Cases replaced by MagicMocks.
    No real MongoDB connection is made at any point.
    """
    mock_create_agent  = MagicMock()
    mock_list_agents   = MagicMock()
    mock_delete_agents = MagicMock()
    mock_create_tool   = MagicMock()
    mock_list_tools    = MagicMock()
    mock_delete_tools  = MagicMock()
    mock_create_kb     = MagicMock()
    mock_list_kbs      = MagicMock()
    mock_delete_kbs    = MagicMock()

    app.dependency_overrides.update({
        get_create_agent_use_case:           lambda: mock_create_agent,
        get_list_agents_use_case:            lambda: mock_list_agents,
        delete_agents_use_case:              lambda: mock_delete_agents,
        get_create_tool_use_case:            lambda: mock_create_tool,
        get_list_tools_use_case:             lambda: mock_list_tools,
        get_delete_tools_use_case:           lambda: mock_delete_tools,
        get_create_knowledge_base_use_case:  lambda: mock_create_kb,
        get_list_knowledge_bases_use_case:   lambda: mock_list_kbs,
        get_delete_knowledge_bases_use_case: lambda: mock_delete_kbs,
    })

    with TestClient(app, base_url="http://testserver") as tc:
        tc.mock_create_agent  = mock_create_agent
        tc.mock_list_agents   = mock_list_agents
        tc.mock_delete_agents = mock_delete_agents
        tc.mock_create_tool   = mock_create_tool
        tc.mock_list_tools    = mock_list_tools
        tc.mock_delete_tools  = mock_delete_tools
        tc.mock_create_kb     = mock_create_kb
        tc.mock_list_kbs      = mock_list_kbs
        tc.mock_delete_kbs    = mock_delete_kbs
        yield tc

    app.dependency_overrides.clear()
