from typing import Any, Dict

from app.core.logging import get_logger
from app.exceptions.knowledge_bases import KnowledgeBaseNotExists
from app.repositories.knowledge_bases.mongo import KnowledgeBasesMongoRepository

logger = get_logger("delete_knowledge_bases")


class DeleteKnowledgeBasesUseCase:
    def __init__(self, knowledge_bases_repository: KnowledgeBasesMongoRepository):
        self.knowledge_bases_repository = knowledge_bases_repository

    def execute(self, filters: Dict[str, Any]) -> dict:
        logger.info(f"Attempting to delete knowledge bases with filters: {filters}")

        try:
            return self.knowledge_bases_repository.delete(filters)
        except KnowledgeBaseNotExists as e:
            logger.error(f"Failed to delete knowledge base(s): {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting knowledge base(s): {str(e)}")
            raise
