"""Unit tests for agent use cases."""
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.use_cases.agents.create_agent import CreateAgentUseCase
from app.use_cases.agents.list_agents import ListAgentsUseCase
from app.use_cases.agents.delete_agents import DeleteAgentsUseCase
from app.schemas.agents.agent_create import AgentSchema, AgentResponseSchema, AgentsAvatarSchema
from app.schemas.agents.agents_list import AgentsListSchema
from app.entities.agents import AgentsEntity
from app.exceptions.agents import AgentNotExists

# Reusable valid ObjectId (24-char hex)
VALID_OID = "507f1f77bcf86cd799439011"
NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)


@pytest.fixture
def mock_repo():
    return MagicMock()


def _agent_entity(**extra):
    return AgentsEntity(
        _id=VALID_OID,
        name="Test Agent",
        specialty="Dev",
        enable=True,
        avatar=AgentsAvatarSchema(image_url="http://img.com/1"),
        created_at=NOW,
        updated_at=NOW,
        **extra,
    )


def test_create_agent_success(mock_repo):
    entity = _agent_entity()
    mock_repo.create.return_value = entity
    use_case = CreateAgentUseCase(mock_repo)

    agent_data = AgentSchema(
        name="Test Agent",
        specialty="Dev",
        enable=True,
        avatar=AgentsAvatarSchema(image_url="http://img.com/1"),
    )
    result = use_case.execute(agent_data=agent_data)

    assert result.id == VALID_OID
    mock_repo.create.assert_called_once()


def test_list_agents_success(mock_repo):
    entity = _agent_entity()
    mock_repo.list.return_value = [entity]
    mock_repo.count.return_value = 1
    use_case = ListAgentsUseCase(mock_repo)

    result = use_case.execute(limit=10, skip=0, filters={})

    assert result.total_count == 1
    assert len(result.items) == 1
    mock_repo.list.assert_called_once()


def test_delete_agents_success(mock_repo):
    mock_repo.count.return_value = 1
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_delete_result.acknowledged = True
    mock_repo.delete_many.return_value = mock_delete_result
    use_case = DeleteAgentsUseCase(mock_repo)

    result = use_case.execute(filters={"_id": VALID_OID})

    assert result["deleted_count"] == 1
    assert result["acknowledged"] is True
    mock_repo.delete_many.assert_called_once()


def test_delete_agents_not_found(mock_repo):
    mock_repo.count.return_value = 0
    use_case = DeleteAgentsUseCase(mock_repo)

    with pytest.raises(AgentNotExists):
        use_case.execute(filters={"_id": VALID_OID})
