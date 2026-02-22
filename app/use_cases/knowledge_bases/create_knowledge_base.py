from app.core.logging import get_logger
from app.exceptions.knowledge_bases import KnowledgeBaseNotExists
from app.repositories.knowledge_bases.mongo import KnowledgeBasesMongoRepository
from app.schemas.knowledge_bases.knowledge_base_create import (
    KnowledgeBaseSchema,
    KnowledgeBaseResponseSchema,
)

logger = get_logger("create_knowledge_base")


class CreateKnowledgeBaseUseCase:
    def __init__(
        self,
        knowledge_bases_repository: KnowledgeBasesMongoRepository,
    ):
        self.knowledge_bases_repository = knowledge_bases_repository

    def execute(self, kb_data: KnowledgeBaseSchema) -> KnowledgeBaseResponseSchema:
        logger.info(f"Creating knowledge base with: {kb_data}")

        try:

            created_kb = self.knowledge_bases_repository.create(
                kb_data.model_dump(by_alias=True, exclude_none=True)
            )

            logger.info(f"Knowledge base created successfully with id: {created_kb.id}")
            return KnowledgeBaseResponseSchema(**created_kb.model_dump())

        except (
            KnowledgeBaseNotExists,
            TypeError,
        ) as e:
            logger.error(f"Failed to create knowledge base: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating knowledge base: {str(e)}")
            raise
