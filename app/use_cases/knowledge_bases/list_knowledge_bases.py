from typing import Any, Dict, Optional

from app.core.logging import get_logger
from app.repositories.knowledge_bases.mongo import KnowledgeBasesMongoRepository
from app.schemas.knowledge_bases.knowledge_bases_list import KnowledgeBasesListSchema

logger = get_logger("list_knowledge_bases")


class ListKnowledgeBasesUseCase:
    def __init__(
        self,
        knowledge_bases_repository: KnowledgeBasesMongoRepository,
    ):
        self.knowledge_bases_repository = knowledge_bases_repository

    def execute(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        skip: int = 0,
        last_iterations: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[int] = 1,
    ) -> KnowledgeBasesListSchema:
        logger.info(
            f"Listing knowledge bases with limit: {limit}, "
            f"skip: {skip}, "
            f"last_iterations: {last_iterations}, "
            f"order_by: {order_by}, "
            f"order_dir: {order_dir}, "
            f"filters: {filters}"
        )

        try:
            (
                knowledge_bases,
                total_count,
            ) = self.knowledge_bases_repository.get_list(
                filters=filters,
                limit=limit,
                skip=skip,
                last_iterations=last_iterations,
                order_by=order_by,
                order_dir=order_dir,
            )

            return KnowledgeBasesListSchema(items=knowledge_bases, total_count=total_count)

        except Exception as e:
            logger.error(f"Failed to list knowledge bases: {str(e)}")
            raise
