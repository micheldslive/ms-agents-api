"""Integration tests for the /api/v1/agents/ endpoints."""
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.schemas.agents.agent_create import AgentResponseSchema, AgentsAvatarSchema
from app.schemas.agents.agents_list import AgentsListSchema
from app.entities.agents import AgentsEntity

BASE = "/api/v1/agents/"
VALID_OID = "507f1f77bcf86cd799439011"
NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)

# ── helpers ──────────────────────────────────────────────────────────────────
def _agent_response():
    return AgentResponseSchema(
        id=VALID_OID,
        name="Integration Agent",
        specialty="Testing",
        enable=True,
        avatar=AgentsAvatarSchema(image_url="http://img.com/test"),
        created_at=NOW,
    )

def _agents_list():
    entity = AgentsEntity(
        _id=VALID_OID,
        name="Integration Agent",
        specialty="Testing",
        enable=True,
        avatar=AgentsAvatarSchema(image_url="http://img.com/test"),
        created_at=NOW,
        updated_at=NOW,
    )
    return AgentsListSchema(items=[entity], total_count=1)


# ── tests ─────────────────────────────────────────────────────────────────────
def test_create_agent_returns_200(client: TestClient):
    client.mock_create_agent.execute.return_value = _agent_response()

    response = client.post(BASE, json={
        "name": "Integration Agent",
        "specialty": "Testing",
        "enable": True,
        "avatar": {"image_url": "http://img.com/test"},
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Integration Agent"
    assert data["id"] == VALID_OID
    client.mock_create_agent.execute.assert_called_once()


def test_list_agents_returns_200_with_items(client: TestClient):
    client.mock_list_agents.execute.return_value = _agents_list()

    response = client.get(BASE)

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total_count" in data
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    client.mock_list_agents.execute.assert_called_once()


def test_delete_agent_returns_deleted_count(client: TestClient):
    client.mock_delete_agents.execute.return_value = {
        "deleted_count": 1,
        "acknowledged": True,
    }

    # Must use a valid 24-char hex ObjectId
    response = client.delete(f"{BASE}?_id={VALID_OID}")

    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] == 1
    assert data["acknowledged"] is True
    client.mock_delete_agents.execute.assert_called_once()
