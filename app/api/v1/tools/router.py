from typing import Any
from fastapi import APIRouter

from app.schemas.tools.tool_create import ToolResponseSchema
from app.schemas.tools.tools_list import ToolsListSchema

from .endpoints import (
    create_tool,
    delete_tools,
    list_tools,
)

router = APIRouter(prefix="/tools", tags=["Tools"])

router.add_api_route(
    "/",
    create_tool,
    methods=["POST"],
    name="Create Tool",
    description="Creates a new tool.",
    response_model=ToolResponseSchema,
)

router.add_api_route(
    "/",
    list_tools,
    methods=["GET"],
    name="List Tools",
    description="Returns the tools if parameters is provided.",
    response_model=ToolsListSchema,
)

router.add_api_route(
    "/",
    delete_tools,
    methods=["DELETE"],
    name="Delete Tools",
    description="Delete tool(s) of a specific _id.",
    response_model=Any,
)
