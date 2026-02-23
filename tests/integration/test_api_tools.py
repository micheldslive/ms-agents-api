"""Integration tests for the /api/v1/tools/ endpoints."""
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.schemas.tools.tool_create import ToolResponseSchema, ToolTypeEnum
from app.schemas.tools.tools_list import ToolsListSchema
from app.entities.tools import ToolsEntity

BASE = "/api/v1/tools/"
VALID_OID = "507f1f77bcf86cd799439011"
NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _tool_response():
    return ToolResponseSchema(
        id=VALID_OID,
        name="Integration Tool",
        description="A tool for testing",
        type=ToolTypeEnum.http,
        enable=True,
        created_at=NOW,
        updated_at=NOW,
    )


def _tools_list():
    entity = ToolsEntity(
        _id=VALID_OID,
        name="Integration Tool",
        description="A tool for testing",
        type=ToolTypeEnum.http,
        enable=True,
        created_at=NOW,
        updated_at=NOW,
    )
    return ToolsListSchema(items=[entity], total_count=1)


def test_create_tool_returns_200(client: TestClient):
    client.mock_create_tool.execute.return_value = _tool_response()

    response = client.post(BASE, json={
        "name": "Integration Tool",
        "description": "A tool for testing",
        "type": "http",
        "enable": True,
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Integration Tool"
    assert data["id"] == VALID_OID
    client.mock_create_tool.execute.assert_called_once()


def test_list_tools_returns_200_with_items(client: TestClient):
    client.mock_list_tools.execute.return_value = _tools_list()

    response = client.get(BASE)

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total_count" in data
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    client.mock_list_tools.execute.assert_called_once()


def test_delete_tool_returns_deleted_count(client: TestClient):
    client.mock_delete_tools.execute.return_value = {
        "deleted_count": 1,
        "acknowledged": True,
    }

    response = client.delete(f"{BASE}?_id={VALID_OID}")

    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] == 1
    assert data["acknowledged"] is True
    client.mock_delete_tools.execute.assert_called_once()
