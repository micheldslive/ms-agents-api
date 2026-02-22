from app.core.logging import get_logger
from app.exceptions.tools import ToolNotExists
from app.repositories.tools.mongo import ToolsMongoRepository
from app.schemas.tools.tool_create import (
    ToolSchema,
    ToolResponseSchema,
)

logger = get_logger("create_tool")


class CreateToolUseCase:
    def __init__(
        self,
        tools_repository: ToolsMongoRepository,
    ):
        self.tools_repository = tools_repository

    def execute(self, tool_data: ToolSchema) -> ToolResponseSchema:
        logger.info(f"Creating tool with: {tool_data}")

        try:

            created_tool = self.tools_repository.create(
                tool_data.model_dump(by_alias=True, exclude_none=True)
            )

            logger.info(f"Tool created successfully with id: {created_tool.id}")
            return ToolResponseSchema(**created_tool.model_dump())

        except (
            ToolNotExists,
            TypeError,
        ) as e:
            logger.error(f"Failed to create tool: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating tool: {str(e)}")
            raise
