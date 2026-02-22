from typing import Annotated

from fastapi import Depends

from app.api.dependencies.repositories import (
    get_tools_repository,
)

from app.repositories.tools.mongo import ToolsMongoRepository
from app.use_cases.tools.create_tool import CreateToolUseCase
from app.use_cases.tools.delete_tools import DeleteToolsUseCase
from app.use_cases.tools.list_tools import ListToolsUseCase


def get_create_tool_use_case(
    tools_repository: Annotated[ToolsMongoRepository, Depends(get_tools_repository)],
):
    return CreateToolUseCase(
        tools_repository=tools_repository,
    )


def get_list_tools_use_case(
    tools_repository: Annotated[ToolsMongoRepository, Depends(get_tools_repository)],
):
    return ListToolsUseCase(tools_repository=tools_repository)


def delete_tools_use_case(
    tools_repository: Annotated[ToolsMongoRepository, Depends(get_tools_repository)],
):
    return DeleteToolsUseCase(tools_repository=tools_repository)
