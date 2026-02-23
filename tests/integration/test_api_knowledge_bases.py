"""Integration tests for the /api/v1/knowledge-bases/ endpoints."""
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.schemas.knowledge_bases.knowledge_base_create import (
    KnowledgeBaseResponseSchema,
    KnowledgeBaseTypeEnum,
)
from app.schemas.knowledge_bases.knowledge_bases_list import KnowledgeBasesListSchema
from app.entities.knowledge_bases import KnowledgeBasesEntity

BASE = "/api/v1/knowledge-bases/"
VALID_OID = "507f1f77bcf86cd799439011"
NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _kb_response():
    return KnowledgeBaseResponseSchema(
        id=VALID_OID,
        name="Integration KB",
        description="A KB for testing",
        type=KnowledgeBaseTypeEnum.document,
        enable=True,
        created_at=NOW,
        updated_at=NOW,
    )


def _kbs_list():
    entity = KnowledgeBasesEntity(
        _id=VALID_OID,
        name="Integration KB",
        description="A KB for testing",
        type=KnowledgeBaseTypeEnum.document,
        enable=True,
        created_at=NOW,
        updated_at=NOW,
    )
    return KnowledgeBasesListSchema(items=[entity], total_count=1)


def test_create_knowledge_base_returns_200(client: TestClient):
    client.mock_create_kb.execute.return_value = _kb_response()

    response = client.post(BASE, json={
        "name": "Integration KB",
        "description": "A KB for testing",
        "type": "document",
        "enable": True,
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Integration KB"
    assert data["id"] == VALID_OID
    client.mock_create_kb.execute.assert_called_once()


def test_list_knowledge_bases_returns_200_with_items(client: TestClient):
    client.mock_list_kbs.execute.return_value = _kbs_list()

    response = client.get(BASE)

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total_count" in data
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    client.mock_list_kbs.execute.assert_called_once()


def test_delete_knowledge_base_returns_deleted_count(client: TestClient):
    client.mock_delete_kbs.execute.return_value = {
        "deleted_count": 1,
        "acknowledged": True,
    }

    response = client.delete(f"{BASE}?_id={VALID_OID}")

    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] == 1
    assert data["acknowledged"] is True
    client.mock_delete_kbs.execute.assert_called_once()
