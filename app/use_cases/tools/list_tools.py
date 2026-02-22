from typing import Any, Dict, Optional

from app.core.logging import get_logger
from app.repositories.tools.mongo import ToolsMongoRepository
from app.schemas.tools.tools_list import ToolsListSchema

logger = get_logger("list_tools")


class ListToolsUseCase:
    def __init__(
        self,
        tools_repository: ToolsMongoRepository,
    ):
        self.tools_repository = tools_repository

    def execute(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        skip: int = 0,
        last_iterations: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[int] = 1,
    ) -> ToolsListSchema:
        logger.info(
            f"Listing tools with limit: {limit}, "
            f"skip: {skip}, "
            f"last_iterations: {last_iterations}, "
            f"order_by: {order_by}, "
            f"order_dir: {order_dir}, "
            f"filters: {filters}"
        )

        try:
            (
                tools,
                total_count,
            ) = self.tools_repository.get_list(
                filters=filters,
                limit=limit,
                skip=skip,
                last_iterations=last_iterations,
                order_by=order_by,
                order_dir=order_dir,
            )

            return ToolsListSchema(items=tools, total_count=total_count)

        except Exception as e:
            logger.error(f"Failed to list tools: {str(e)}")
            raise
