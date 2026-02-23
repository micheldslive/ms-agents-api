"""Unit tests for knowledge base use cases."""
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.use_cases.knowledge_bases.create_knowledge_base import CreateKnowledgeBaseUseCase
from app.use_cases.knowledge_bases.list_knowledge_bases import ListKnowledgeBasesUseCase
from app.use_cases.knowledge_bases.delete_knowledge_bases import DeleteKnowledgeBasesUseCase
from app.schemas.knowledge_bases.knowledge_base_create import (
    KnowledgeBaseSchema,
    KnowledgeBaseResponseSchema,
    KnowledgeBaseTypeEnum,
)
from app.schemas.knowledge_bases.knowledge_bases_list import KnowledgeBasesListSchema
from app.entities.knowledge_bases import KnowledgeBasesEntity
from app.exceptions.knowledge_bases import KnowledgeBaseNotExists

VALID_OID = "507f1f77bcf86cd799439011"
NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)


@pytest.fixture
def mock_repo():
    return MagicMock()


def _kb_entity(**extra):
    return KnowledgeBasesEntity(
        _id=VALID_OID,
        name="KB1",
        description="Desc",
        type=KnowledgeBaseTypeEnum.document,
        enable=True,
        created_at=NOW,
        updated_at=NOW,
        **extra,
    )


def test_create_kb_success(mock_repo):
    entity = _kb_entity()
    mock_repo.create.return_value = entity
    use_case = CreateKnowledgeBaseUseCase(mock_repo)

    kb_data = KnowledgeBaseSchema(
        name="KB1",
        description="Desc",
        type=KnowledgeBaseTypeEnum.document,
        enable=True,
    )
    result = use_case.execute(kb_data=kb_data)

    assert result.id == VALID_OID
    mock_repo.create.assert_called_once()


def test_list_kbs_success(mock_repo):
    entity = _kb_entity()
    mock_repo.get_list.return_value = ([entity], 1)
    use_case = ListKnowledgeBasesUseCase(mock_repo)

    result = use_case.execute(filters={}, limit=10, skip=0)

    assert result.total_count == 1
    assert len(result.items) == 1
    mock_repo.get_list.assert_called_once()


def test_delete_kbs_success(mock_repo):
    mock_repo.delete.return_value = {"deleted_count": 1, "acknowledged": True}
    use_case = DeleteKnowledgeBasesUseCase(mock_repo)

    result = use_case.execute(filters={"_id": VALID_OID})

    assert result["deleted_count"] == 1
    mock_repo.delete.assert_called_once()


def test_delete_kbs_not_found(mock_repo):
    mock_repo.delete.side_effect = KnowledgeBaseNotExists()
    use_case = DeleteKnowledgeBasesUseCase(mock_repo)

    with pytest.raises(KnowledgeBaseNotExists):
        use_case.execute(filters={"_id": VALID_OID})
