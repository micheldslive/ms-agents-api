from typing import Any, Dict

from app.core.logging import get_logger
from app.exceptions.tools import ToolNotExists
from app.repositories.tools.mongo import ToolsMongoRepository

logger = get_logger("delete_tools")


class DeleteToolsUseCase:
    def __init__(self, tools_repository: ToolsMongoRepository):
        self.tools_repository = tools_repository

    def execute(self, filters: Dict[str, Any]) -> dict:
        logger.info(f"Attempting to delete tools with filters: {filters}")

        try:
            return self.tools_repository.delete(filters)
        except ToolNotExists as e:
            logger.error(f"Failed to delete tool(s): {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting tool(s): {str(e)}")
            raise
