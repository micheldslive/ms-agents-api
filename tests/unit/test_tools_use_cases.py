"""Unit tests for tool use cases."""
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.use_cases.tools.create_tool import CreateToolUseCase
from app.use_cases.tools.list_tools import ListToolsUseCase
from app.use_cases.tools.delete_tools import DeleteToolsUseCase
from app.schemas.tools.tool_create import ToolSchema, ToolTypeEnum, ToolResponseSchema
from app.schemas.tools.tools_list import ToolsListSchema
from app.entities.tools import ToolsEntity
from app.exceptions.tools import ToolNotExists

VALID_OID = "507f1f77bcf86cd799439011"
NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)


@pytest.fixture
def mock_repo():
    return MagicMock()


def _tool_entity(**extra):
    return ToolsEntity(
        _id=VALID_OID,
        name="Tool1",
        description="Desc",
        type=ToolTypeEnum.http,
        enable=True,
        created_at=NOW,
        updated_at=NOW,
        **extra,
    )


def test_create_tool_success(mock_repo):
    entity = _tool_entity()
    mock_repo.create.return_value = entity
    use_case = CreateToolUseCase(mock_repo)

    tool_data = ToolSchema(
        name="Tool1",
        description="Desc",
        type=ToolTypeEnum.http,
        enable=True,
    )
    result = use_case.execute(tool_data=tool_data)

    assert result.id == VALID_OID
    mock_repo.create.assert_called_once()


def test_list_tools_success(mock_repo):
    entity = _tool_entity()
    mock_repo.get_list.return_value = ([entity], 1)
    use_case = ListToolsUseCase(mock_repo)

    result = use_case.execute(filters={}, limit=10, skip=0)

    assert result.total_count == 1
    assert len(result.items) == 1
    mock_repo.get_list.assert_called_once()


def test_delete_tools_success(mock_repo):
    mock_repo.delete.return_value = {"deleted_count": 1, "acknowledged": True}
    use_case = DeleteToolsUseCase(mock_repo)

    result = use_case.execute(filters={"_id": VALID_OID})

    assert result["deleted_count"] == 1
    mock_repo.delete.assert_called_once()


def test_delete_tools_not_found(mock_repo):
    mock_repo.delete.side_effect = ToolNotExists()
    use_case = DeleteToolsUseCase(mock_repo)

    with pytest.raises(ToolNotExists):
        use_case.execute(filters={"_id": VALID_OID})
